/**
 * Flujo de venta de certificados — una sola decisión por pantalla.
 *
 *   inicio → examen → (fallo) → nombre → contacto → pago → comprobante | transferencia → listo
 *
 * Cada curso es una página que define `window.CURSO` (precio, preguntas, textos)
 * y carga este archivo. Ver certificado-manipulacion-de-alimentos.html.
 *
 * Integraciones (las mismas de las páginas anteriores):
 *   - n8n (Telegram): trackEvent()
 *   - CRM: createCrmLead() al completar los datos y markLeadAsProposal() al iniciar el pago
 *   - Meta: Pixel 'Lead' (con event_id compartido con la CAPI del CRM) e 'InitiateCheckout'
 *   - Pago: link de PSE (el usuario escribe el valor) o transferencia Bancolombia,
 *           verificados a mano con el comprobante que llega por WhatsApp.
 */
(function () {
    const C = window.CURSO;

    const N8N_WEBHOOK     = 'https://n8n.certitecol.com/webhook/6a03322d-f85e-46df-a0f4-fb27010a6b0c';
    const CRM_LEADS_URL   = 'https://controla-570877385695.northamerica-northeast1.run.app/api/crm/leads/publico';
    const CRM_BUSINESS_ID = 3;

    const PRECIO_NUM = C.precio.toLocaleString('es-CO');   // "25.000"
    const PRECIO_TXT = '$' + PRECIO_NUM;                   // "$25.000"
    const TOTAL      = C.preguntas.length;
    const MIN_OK     = Math.ceil(TOTAL * C.minAprobar);
    const IS_MOBILE  = /Android|iPhone|iPad|iPod|Opera Mini|IEMobile/i.test(navigator.userAgent);

    // Paso de la barra de progreso y a dónde lleva "Atrás"
    const PASO  = { inicio: 0, examen: 1, fallo: 1, nombre: 2, contacto: 2, pago: 3, comprobante: 3, transferencia: 3, listo: 4 };
    const ATRAS = { contacto: 'nombre', pago: 'contacto', comprobante: 'pago', transferencia: 'pago' };
    const NOMBRE_PASO = ['', 'Examen', 'Tus datos', 'Pago', 'Listo'];

    const DOCS = {
        CC:  'Cédula de Ciudadanía',
        TI:  'Tarjeta de Identidad',
        CE:  'Cédula de Extranjería',
        PPT: 'Permiso por Protección Temporal (PPT)',
        PAS: 'Pasaporte'
    };

    // ════════════════ Estado ════════════════
    function initialState() {
        return {
            screen: 'inicio',
            quiz: { idx: 0, score: 0 },
            user: { type: 'CC', num: '', name: '', phone: '', email: '' },
            consent: null,
            leadCreated: false,
            leadId: null,
            leadProposed: false,
            leadEventId: null,
            checkoutTracked: {},
            metodo: null,      // 'PSE' | 'Bancolombia'
            pago: null         // null | 'iniciado' | 'comprobante_enviado'
        };
    }

    let S = loadState();

    function loadState() {
        let saved = null;
        try { saved = JSON.parse(localStorage.getItem(C.storageKey)); } catch (e) {}
        if (!saved) saved = migrateLegacy();
        const s = Object.assign(initialState(), saved || {});
        s.user = Object.assign(initialState().user, s.user || {});
        if (!(s.screen in PASO)) s.screen = 'inicio';
        return s;
    }

    // Visitantes que iban a mitad del proceso en la versión anterior de la página:
    // conservamos su avance y su lead (para no duplicarlo en el CRM ni en Meta).
    function migrateLegacy() {
        if (!C.legacyStorageKey) return null;
        let old = null;
        try { old = JSON.parse(localStorage.getItem(C.legacyStorageKey)); } catch (e) {}
        if (!old || typeof old !== 'object') return null;

        const u = old.userData || {};
        const s = initialState();
        s.user = { type: u.type || 'CC', num: u.num || '', name: u.name || '', phone: u.phone || '', email: u.email || '' };
        s.consent = old.consent || null;
        s.leadCreated = !!old.leadCreated;
        s.leadId = old.leadId || null;
        s.leadProposed = !!old.leadProposed;
        s.leadEventId = old.leadEventId || null;
        s.metodo = old.metodoPago || null;
        s.pago = old.psePago || null;
        s.quiz = { idx: C.preguntas.length, score: (old.quiz && old.quiz.score) || 0 };

        if (old.view === 'view-checkout' && u.name && u.email) {
            s.screen = s.pago === 'comprobante_enviado' ? 'listo' : s.pago === 'iniciado' ? 'comprobante' : 'pago';
        } else if (old.view === 'view-registration') {
            s.screen = 'nombre';
        } else {
            return null;   // examen a medias o no aprobado: empieza de cero
        }
        try {
            localStorage.setItem(C.storageKey, JSON.stringify(s));
            localStorage.removeItem(C.legacyStorageKey);
        } catch (e) {}
        return s;
    }

    function save() {
        try { localStorage.setItem(C.storageKey, JSON.stringify(S)); } catch (e) {}
    }

    // ════════════════ Utilidades ════════════════
    const $ = id => document.getElementById(id);

    function esc(v) {
        return String(v == null ? '' : v).replace(/[&<>"']/g, ch => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch]));
    }

    // El nombre va tal cual al certificado: "laura GÓMEZ" → "Laura Gómez"
    function toTitleCase(value) {
        return String(value || '').trim().replace(/\s+/g, ' ').toLocaleLowerCase('es-CO')
            .replace(/(^|[\s-])(\p{L})/gu, (m, sep, ch) => sep + ch.toLocaleUpperCase('es-CO'));
    }

    function firstName() { return (S.user.name || '').split(' ')[0]; }
    function docLabel()  { return S.user.num ? 'Documento: ' + S.user.type + ' ' + S.user.num : ''; }
    function docIsNumeric(type) { return type === 'CC' || type === 'TI'; }

    function fbqSafe() { try { if (window.fbq) window.fbq.apply(null, arguments); } catch (e) {} }

    function legacyCopy(text) {
        const ta = document.createElement('textarea');
        ta.value = text;
        ta.setAttribute('readonly', '');
        ta.style.position = 'fixed';
        ta.style.opacity = '0';
        document.body.appendChild(ta);
        ta.select();
        let ok = false;
        try { ok = document.execCommand('copy'); } catch (e) {}
        ta.remove();
        return ok;
    }

    function copyText(text) {
        if (navigator.clipboard && window.isSecureContext) {
            return navigator.clipboard.writeText(text).then(() => true, () => legacyCopy(text));
        }
        return Promise.resolve(legacyCopy(text));
    }

    function openWhatsApp(phone, msg) {
        const text = encodeURIComponent(msg);
        // En móvil el deep link abre el chat directo; en escritorio wa.me en otra pestaña
        if (IS_MOBILE) window.location.href = 'whatsapp://send?phone=' + phone + '&text=' + text;
        else window.open('https://wa.me/' + phone + '?text=' + text, '_blank');
    }

    // ════════════════ Tracking (n8n) ════════════════
    function trackEvent(evento, extra) {
        const payload = Object.assign({
            evento: evento,
            pagina: C.pagina,
            version: 'flujo-v2',
            fecha: new Date().toLocaleString('es-CO', { timeZone: 'America/Bogota' }),
            usuario: S.user
        }, extra || {});
        // text/plain evita el preflight de CORS
        fetch(N8N_WEBHOOK, { method: 'POST', headers: { 'Content-Type': 'text/plain' }, body: JSON.stringify(payload), keepalive: true }).catch(() => {});
    }

    // ════════════════ Meta (Pixel + datos para la CAPI) ════════════════
    function getCookie(name) {
        const m = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
        return m ? decodeURIComponent(m.pop()) : '';
    }
    function getFbc() {
        const cookie = getCookie('_fbc');
        if (cookie) return cookie;
        const fbclid = new URLSearchParams(window.location.search).get('fbclid');
        return fbclid ? 'fb.1.' + Date.now() + '.' + fbclid : '';
    }
    // event_id compartido entre el Pixel y la CAPI para que Meta deduplique el 'Lead'
    function getLeadEventId() {
        if (!S.leadEventId) {
            S.leadEventId = 'lead-' + Date.now() + '-' + Math.random().toString(36).slice(2, 10);
            save();
        }
        return S.leadEventId;
    }

    // ════════════════ CRM ════════════════
    let crmLeadInFlight = false;

    function createCrmLead() {
        if (S.leadCreated || crmLeadInFlight) return;
        crmLeadInFlight = true;
        const u = S.user;
        fetch(CRM_LEADS_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            keepalive: true,
            body: JSON.stringify({
                business_id: CRM_BUSINESS_ID,
                servicio: C.slug,
                nombre: u.name,
                tipo_documento: u.type,
                numero_documento: u.num,
                empresa: '',
                telefono: u.phone || '',
                email: u.email,
                origen: 'WEB',
                valor_estimado: C.precio,
                notas: C.producto + ' | Examen aprobado | Flujo v2' +
                       (S.consent ? ' | Autorizó tratamiento de datos (Ley 1581) ' + S.consent.fecha : ''),
                fbc: getFbc(),
                fbp: getCookie('_fbp'),
                event_id: getLeadEventId()
            })
        })
        .then(res => res.ok ? res.json() : Promise.reject(new Error('HTTP ' + res.status)))
        .then(data => {
            S.leadCreated = true;
            const leadId = data?.id ?? data?.lead_id ?? data?.data?.id ?? data?.lead?.id ?? null;
            if (leadId) S.leadId = leadId;
            save();
            // Si ya tocó "Pagar" mientras el CRM respondía, avanzamos el lead ahora
            if (S.pago) markLeadAsProposal();
        })
        .catch(err => trackEvent('crm_lead_error', { detalle: String((err && err.message) || err) }))
        .finally(() => { crmLeadInFlight = false; });
    }

    function markLeadAsProposal() {
        if (S.leadProposed || !S.leadId) return;
        S.leadProposed = true;
        save();
        fetch(CRM_LEADS_URL + '/' + S.leadId, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ business_id: CRM_BUSINESS_ID, estado: 'PROPUESTA' }),
            keepalive: true
        }).catch(() => { S.leadProposed = false; save(); });
    }

    function trackCheckout(metodo) {
        if (!S.checkoutTracked[metodo]) {
            trackEvent('payment_initiated', { metodo: metodo });
            if (!Object.keys(S.checkoutTracked).length) {
                fbqSafe('track', 'InitiateCheckout', { content_name: C.producto, value: C.precio, currency: 'COP', num_items: 1 });
            }
            S.checkoutTracked[metodo] = true;
        }
        markLeadAsProposal();
        save();
    }

    // ════════════════ Navegación ════════════════
    // Pantallas con "Atrás" crean una entrada en el historial: el botón atrás de
    // Android vuelve al paso anterior en vez de sacar al usuario de la página.
    function go(screen, push) {
        if (S.screen === screen) return render();
        S.screen = screen;
        save();
        if (ATRAS[screen] && push !== false) history.pushState({ screen: screen }, '');
        render();
    }

    function back() {
        const prev = ATRAS[S.screen];
        if (!prev) return;
        if (history.state && history.state.screen === S.screen) history.back();
        else go(prev, false);
    }

    window.addEventListener('popstate', () => {
        const prev = ATRAS[S.screen];
        if (prev) { S.screen = prev; save(); render(); }
    });

    // ════════════════ Vistas ════════════════
    function certPreview() {
        const name = toTitleCase(S.user.name);
        return `
        <div class="cert" aria-label="Vista previa de tu certificado">
            <div class="cert-paper">
                <div class="cert-brand">CERTIFICADO</div>
                <p class="cert-kicker">Otorgado a</p>
                <p id="cert-name" class="cert-name ${name ? '' : 'empty'}">${esc(name || 'Tu nombre aquí')}</p>
                <p id="cert-doc" class="cert-doc">${esc(docLabel())}</p>
                <p class="cert-body">${C.certTexto}</p>
                <div class="cert-foot"><span class="cert-seal"><i class="fas fa-award"></i></span><span class="cert-sign"></span></div>
                <div class="cert-mark" aria-hidden="true">MUESTRA</div>
            </div>
        </div>`;
    }

    // En la pantalla de pago no se muestra el certificado: solo una tarjeta bloqueada
    function lockedCert() {
        return `
        <div class="cert-locked">
            <div class="cl-doc" aria-hidden="true">
                <span class="cl-bar w40"></span><span class="cl-bar w70 dark"></span><span class="cl-bar w50"></span>
                <span class="cl-bar w90"></span><span class="cl-bar w80"></span><span class="cl-bar w60"></span>
            </div>
            <div class="cl-overlay">
                <span class="cl-lock"><i class="fas fa-lock"></i></span>
                <b>${C.producto}</b>
                <span>Te enviamos ${C.entrega} en PDF a tu correo cuando confirmemos tu pago</span>
            </div>
        </div>`;
    }

    const VIEWS = {
        inicio: () => `
            <section class="screen">
                <span class="pill"><i class="fas fa-shield-halved"></i> ${C.aval}</span>
                <h1 class="h1">Tu certificado de <span>${C.titulo || C.nombre}</span>, hoy mismo</h1>
                <p class="lead">Presenta un examen corto y gratis. Si apruebas, pagas ${PRECIO_TXT} y te enviamos ${C.entrega} en PDF a tu correo.</p>
                ${certPreview()}
                <ul class="facts">
                    <li><i class="fas fa-stopwatch"></i><span><b>${TOTAL} preguntas</b> · ${C.minutos} minutos</span></li>
                    <li><i class="fas fa-hand-holding-dollar"></i><span><b>Pagas solo si apruebas</b> · ${PRECIO_TXT}</span></li>
                    <li><i class="fas fa-envelope-circle-check"></i><span><b>Llega a tu correo</b> el mismo día</span></li>
                </ul>
            </section>
            <div class="actions">
                <button class="btn btn-primary" onclick="F.startExam()">Empezar examen gratis <i class="fas fa-arrow-right"></i></button>
                <p class="fine"><i class="fas fa-shield-halved"></i> Certificado verificable en línea · <a href="../verificacion.html" target="_blank">Verificar uno</a></p>
            </div>`,

        examen: () => {
            const q = C.preguntas[S.quiz.idx];
            return `
            <section class="screen">
                <p class="q-count">Pregunta ${S.quiz.idx + 1} de ${TOTAL}</p>
                <h2 class="q-title">${q.q}</h2>
                ${q.svg ? `<div class="q-figure">${q.svg}</div>` : ''}
                <div class="options" id="options">
                    ${q.options.map((o, i) => `
                        <button class="opt" onclick="F.answer(${i})"><span class="opt-key">${String.fromCharCode(65 + i)}</span><span>${o}</span></button>`).join('')}
                </div>
                <p id="q-feedback" class="q-feedback" hidden></p>
            </section>`;
        },

        fallo: () => `
            <section class="screen center">
                <div class="result-icon warn"><i class="fas fa-rotate-right"></i></div>
                <h1 class="h2">¡Casi lo logras!</h1>
                <p class="lead">Obtuviste <b>${S.quiz.score} de ${TOTAL}</b>. Necesitas ${MIN_OK} para aprobar. Puedes intentarlo otra vez, es gratis.</p>
            </section>
            <div class="actions">
                <button class="btn btn-primary" onclick="F.retry()"><i class="fas fa-rotate-right"></i> Intentar de nuevo</button>
            </div>`,

        nombre: () => `
            <section class="screen">
                <div class="success-banner">
                    <i class="fas fa-circle-check"></i>
                    <div><b>¡Aprobaste con ${S.quiz.score}/${TOTAL}!</b><span>Ahora, ¿cómo debe aparecer tu nombre?</span></div>
                </div>
                ${certPreview()}
                <form id="f-nombre" class="form" onsubmit="F.submitNombre(event)">
                    <label class="field">
                        <span class="label">Nombre completo</span>
                        <input id="in-name" class="input" required autocomplete="name" autocapitalize="words"
                               placeholder="Nombres y apellidos" value="${esc(S.user.name)}" oninput="F.onName(this)">
                    </label>
                    <div class="field" id="doctype-field" ${S.user.type === 'CC' ? 'hidden' : ''}>
                        <label class="label" for="in-doctype">Tipo de documento</label>
                        <select id="in-doctype" class="input" onchange="F.onDocType(this)">
                            ${Object.keys(DOCS).map(k => `<option value="${k}" ${S.user.type === k ? 'selected' : ''}>${DOCS[k]}</option>`).join('')}
                        </select>
                    </div>
                    <label class="field">
                        <span class="label" id="doc-label">${S.user.type === 'CC' ? 'Número de cédula' : 'Número de documento'}</span>
                        <input id="in-doc" class="input" required autocomplete="off" maxlength="20" placeholder="Sin puntos ni espacios"
                               value="${esc(S.user.num)}" oninput="F.onDoc(this)">
                    </label>
                    <button type="button" class="link" id="doctype-toggle" onclick="F.showDocType()" ${S.user.type === 'CC' ? '' : 'hidden'}>¿No tienes cédula? Usa otro documento</button>
                </form>
            </section>
            <div class="actions">
                <button class="btn btn-primary" type="submit" form="f-nombre">Continuar <i class="fas fa-arrow-right"></i></button>
            </div>`,

        contacto: () => `
            <section class="screen">
                <button class="back" onclick="F.back()"><i class="fas fa-arrow-left"></i> Atrás</button>
                <h1 class="h2">¿A dónde te enviamos ${C.entrega}?</h1>
                <p class="sub">Llega en PDF a tu correo y te avisamos por WhatsApp.</p>
                <form id="f-contacto" class="form" onsubmit="F.submitContacto(event)">
                    <label class="field">
                        <span class="label">Correo electrónico</span>
                        <input id="in-email" class="input" type="email" required autocomplete="email" inputmode="email"
                               autocapitalize="off" spellcheck="false" placeholder="tucorreo@gmail.com"
                               value="${esc(S.user.email)}" onblur="F.checkEmail()" oninput="F.onEmailInput()">
                        <button type="button" id="email-suggest" class="email-suggest" hidden onclick="F.applyEmail()"></button>
                    </label>
                    <label class="field">
                        <span class="label">Celular con WhatsApp</span>
                        <span class="input-group">
                            <span class="prefix"><i class="fab fa-whatsapp"></i> +57</span>
                            <input id="in-phone" class="input" type="tel" required inputmode="numeric" autocomplete="tel-national"
                                   pattern="3[0-9]{9}" title="Celular de 10 dígitos que empieza por 3"
                                   placeholder="310 123 4567" value="${esc(S.user.phone)}" oninput="F.onPhone(this)">
                        </span>
                    </label>
                    <label class="consent">
                        <input id="in-consent" type="checkbox" required ${S.consent ? 'checked' : ''}>
                        <span>Autorizo el tratamiento de mis datos para emitir mi certificado y contactarme sobre este proceso (Ley 1581 de 2012).</span>
                    </label>
                    <details class="privacy">
                        <summary>Ver aviso de privacidad</summary>
                        <div>
                            <p><b>Responsable:</b> Alianza Capacitarte, a través de la plataforma CertiTec.</p>
                            <p><b>Datos:</b> tipo y número de documento, nombre, celular y correo.</p>
                            <p><b>Para qué:</b> emitir tu certificado y enviarlo a tu correo, permitir verificar su autenticidad con tu documento, gestionar el pago, contactarte sobre este proceso y medir nuestras campañas.</p>
                            <p><b>Tus derechos:</b> conocer, actualizar, rectificar y pedir la supresión de tus datos, y revocar esta autorización, salvo deber legal de conservarlos.</p>
                            <p><b>Canal de atención:</b> WhatsApp 310 794 1580.</p>
                        </div>
                    </details>
                </form>
            </section>
            <div class="actions">
                <button class="btn btn-primary" type="submit" form="f-contacto">Continuar al pago <i class="fas fa-arrow-right"></i></button>
                <p class="fine"><i class="fas fa-lock"></i> Tus datos están protegidos</p>
            </div>`,

        pago: () => `
            <section class="screen">
                <button class="back" onclick="F.back()"><i class="fas fa-arrow-left"></i> Atrás</button>
                <h1 class="h2">Último paso: el pago</h1>
                ${lockedCert()}
                <div class="summary">
                    <div class="row"><span>A nombre de</span><span class="row-val"><b>${esc(S.user.name)}</b></span></div>
                    <div class="row">
                        <span>Envío a</span>
                        <span class="row-val"><b>${esc(S.user.email)}</b><button class="link" onclick="F.back()">Cambiar</button></span>
                    </div>
                    <div class="row total"><span>Total</span><span class="price">${PRECIO_TXT} <small>COP</small></span></div>
                </div>
                <p class="note"><i class="fas fa-circle-info"></i><span>Al tocar el botón copiamos el valor <b>${PRECIO_NUM}</b> para que lo pegues en PSE. Al terminar, vuelve aquí para enviar tu comprobante.</span></p>
            </section>
            <div class="actions">
                <button class="btn btn-primary" onclick="F.payPSE()"><i class="fas fa-lock"></i> Pagar ${PRECIO_TXT} con PSE</button>
                <button class="btn-link" onclick="F.goTransfer()">Prefiero transferir a Bancolombia</button>
            </div>`,

        comprobante: () => `
            <section class="screen">
                <button class="back" onclick="F.back()"><i class="fas fa-arrow-left"></i> Atrás</button>
                <div class="result-icon info" style="margin:4px 0 16px"><i class="fas fa-receipt"></i></div>
                <h1 class="h2">¿Ya pagaste? Envía tu comprobante</h1>
                <p class="sub">Con el comprobante verificamos tu pago y te enviamos ${C.entrega} a <b>${esc(S.user.email)}</b>.</p>
                <ol class="steps-list">
                    <li><span>1</span>Toma una captura del comprobante de pago.</li>
                    <li><span>2</span>Toca el botón verde y adjunta la captura en el chat.</li>
                </ol>
                <div class="help-box">
                    <p>¿Aún no has pagado?</p>
                    <button class="link" onclick="F.payPSE()">Abrir PSE otra vez (valor ${PRECIO_NUM})</button>
                    <button class="link" onclick="F.goTransfer()">PSE no me funcionó: transferir a Bancolombia</button>
                </div>
            </section>
            <div class="actions">
                <button class="btn btn-wa" onclick="F.sendProof('PSE')"><i class="fab fa-whatsapp"></i> Enviar comprobante</button>
            </div>`,

        transferencia: () => `
            <section class="screen">
                <button class="back" onclick="F.back()"><i class="fas fa-arrow-left"></i> Atrás</button>
                <h1 class="h2">Transfiere ${PRECIO_TXT} a Bancolombia</h1>
                <p class="sub">Desde la app de tu banco. Luego envía el comprobante por WhatsApp.</p>
                <div class="bank-head"><img src="https://images.seeklogo.com/logo-png/42/1/bancolombia-logo-png_seeklogo-428092.png" alt="">Cuenta de ahorros Bancolombia</div>
                <div class="copy-card">
                    <div><span class="muted">Número de cuenta</span><b>${C.banco.mostrar}</b></div>
                    <button class="copy" onclick="F.copy(this, '${C.banco.numero}')"><i class="far fa-copy"></i> Copiar</button>
                </div>
                <div class="copy-card">
                    <div><span class="muted">Valor a transferir</span><b>${PRECIO_TXT}</b></div>
                    <button class="copy" onclick="F.copy(this, '${C.precio}')"><i class="far fa-copy"></i> Copiar</button>
                </div>
            </section>
            <div class="actions">
                <button class="btn btn-wa" onclick="F.sendProof('Bancolombia')"><i class="fab fa-whatsapp"></i> Ya transferí: enviar comprobante</button>
            </div>`,

        listo: () => `
            <section class="screen center">
                <div class="result-icon ok"><i class="fas fa-check"></i></div>
                <h1 class="h2">¡Listo, ${esc(firstName())}!</h1>
                <p class="lead">Estamos verificando tu pago. Apenas lo confirmemos te enviamos ${C.entrega} en PDF a <b>${esc(S.user.email)}</b>.</p>
                <div class="info-card">
                    <i class="fab fa-whatsapp"></i>
                    <span>¿No alcanzaste a adjuntar la captura del comprobante en el chat? Hazlo ahora para que podamos verificar tu pago.</span>
                </div>
            </section>
            <div class="actions">
                <button class="btn btn-outline" onclick="F.sendProof()"><i class="fab fa-whatsapp"></i> Abrir WhatsApp de nuevo</button>
                <button class="btn-link" onclick="F.reset()">Hacer otro certificado</button>
            </div>`
    };

    let answerTimer = null;

    function render() {
        clearTimeout(answerTimer);
        // Recarga justo después de la última respuesta: el examen ya terminó
        if (S.screen === 'examen' && S.quiz.idx >= TOTAL) return finishQuiz();

        const paso = PASO[S.screen];
        const bar = $('progress');
        bar.hidden = paso === 0;
        if (paso) {
            let pct = (paso - 1) / 4 * 100;
            if (S.screen === 'examen') pct += (S.quiz.idx / TOTAL) * 25;
            if (paso === 4) pct = 100;
            bar.classList.toggle('done', paso === 4);
            $('progress-step').textContent = 'Paso ' + Math.min(paso, 4) + ' de 4';
            $('progress-name').textContent = NOMBRE_PASO[paso];
            $('progress-fill').style.width = Math.max(pct, 4) + '%';
        }

        $('main').innerHTML = VIEWS[S.screen]();
        if (S.screen === 'nombre') setupDocInput();
        window.scrollTo(0, 0);
    }

    // ════════════════ Examen ════════════════
    function startExam() {
        trackEvent('exam_started');
        S.quiz = { idx: 0, score: 0 };
        go('examen');
    }

    function answer(i) {
        const q = C.preguntas[S.quiz.idx];
        const buttons = $('options').querySelectorAll('.opt');
        if (buttons[0].disabled) return;
        buttons.forEach(b => { b.disabled = true; });

        const correct = i === q.a;
        buttons[q.a].classList.add('ok');
        if (!correct) buttons[i].classList.add('bad');

        const fb = $('q-feedback');
        fb.className = 'q-feedback ' + (correct ? 'ok' : 'bad');
        fb.innerHTML = correct
            ? '<i class="fas fa-circle-check"></i> ¡Correcto!'
            : '<i class="fas fa-circle-info"></i> La respuesta correcta está marcada en verde';
        fb.hidden = false;

        trackEvent('quiz_answer', { pregunta: S.quiz.idx + 1, result: correct ? 'ok' : 'fail' });

        // El avance se guarda ya; la pausa es solo visual (una recarga no repite la pregunta)
        if (correct) S.quiz.score++;
        S.quiz.idx++;
        save();
        answerTimer = setTimeout(() => {
            if (S.quiz.idx < TOTAL) render();
            else finishQuiz();
        }, correct ? 800 : 1700);
    }

    function finishQuiz() {
        if (S.quiz.score >= MIN_OK) {
            trackEvent('quiz_passed', { score: S.quiz.score + '/' + TOTAL });
            fbqSafe('track', 'Lead', {
                content_ids: [C.slug],
                content_name: C.nombre,
                content_category: 'Cursos',
                content_type: 'product',
                value: C.precio, currency: 'COP'
            }, { eventID: getLeadEventId() });
            go('nombre');
        } else {
            trackEvent('quiz_failed', { score: S.quiz.score + '/' + TOTAL });
            go('fallo');
        }
    }

    function retry() {
        S.quiz = { idx: 0, score: 0 };
        go('examen');
    }

    // ════════════════ Datos: nombre y documento ════════════════
    function sanitizeDoc(value, type) {
        return docIsNumeric(type)
            ? value.replace(/\D/g, '')
            : value.replace(/[^A-Za-z0-9]/g, '').toUpperCase();
    }

    function setupDocInput() {
        const input = $('in-doc');
        if (!input) return;
        const numeric = docIsNumeric(S.user.type);
        input.inputMode = numeric ? 'numeric' : 'text';
        input.pattern = numeric ? '[0-9]{5,12}' : '[A-Za-z0-9]{4,20}';
        input.title = numeric ? 'Solo números, sin puntos ni espacios' : 'Letras y números, sin espacios';
    }

    function onName(input) {
        S.user.name = input.value;
        save();
        const name = toTitleCase(input.value);
        const el = $('cert-name');
        el.textContent = name || 'Tu nombre aquí';
        el.classList.toggle('empty', !name);
    }

    function onDoc(input) {
        const clean = sanitizeDoc(input.value, S.user.type);
        if (clean !== input.value) input.value = clean;
        S.user.num = clean;
        save();
        $('cert-doc').textContent = docLabel();
    }

    function showDocType() {
        $('doctype-field').hidden = false;
        $('doctype-toggle').hidden = true;
        $('in-doctype').focus();
    }

    function onDocType(select) {
        S.user.type = select.value;
        $('doc-label').textContent = S.user.type === 'CC' ? 'Número de cédula' : 'Número de documento';
        setupDocInput();
        onDoc($('in-doc'));
    }

    function submitNombre(e) {
        e.preventDefault();
        S.user.name = toTitleCase($('in-name').value);
        S.user.num = sanitizeDoc($('in-doc').value, S.user.type);
        save();
        trackEvent('datos_nombre');
        go('contacto');
    }

    // ════════════════ Datos: contacto ════════════════
    // Un correo mal escrito = un certificado que nunca llega. Sugerimos la corrección
    // de los dominios más comunes (gmial.com → gmail.com).
    const EMAIL_DOMAINS = ['gmail.com', 'hotmail.com', 'outlook.com', 'yahoo.com', 'icloud.com', 'live.com', 'yahoo.es', 'hotmail.es', 'outlook.es'];
    let emailSuggestShownFor = null;

    function levenshtein(a, b) {
        const dp = Array.from({ length: a.length + 1 }, (_, i) => [i]);
        for (let j = 1; j <= b.length; j++) dp[0][j] = j;
        for (let i = 1; i <= a.length; i++) {
            for (let j = 1; j <= b.length; j++) {
                dp[i][j] = Math.min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
            }
        }
        return dp[a.length][b.length];
    }

    function suggestEmail(value) {
        const at = value.lastIndexOf('@');
        if (at < 1) return null;
        const domain = value.slice(at + 1).toLowerCase();
        if (!domain || EMAIL_DOMAINS.includes(domain)) return null;
        let best = null, bestDist = 3;
        EMAIL_DOMAINS.forEach(d => {
            const dist = levenshtein(domain, d);
            if (dist < bestDist) { best = d; bestDist = dist; }
        });
        return best ? value.slice(0, at + 1) + best : null;
    }

    function checkEmail() {
        const value = $('in-email').value.trim();
        const box = $('email-suggest');
        const suggestion = suggestEmail(value);
        if (!suggestion) { box.hidden = true; return false; }
        box.innerHTML = '¿Quisiste decir <b></b>? Toca para corregir';
        box.querySelector('b').textContent = suggestion;
        box.dataset.value = suggestion;
        box.hidden = false;
        emailSuggestShownFor = value;
        return true;
    }

    function onEmailInput() {
        $('email-suggest').hidden = true;
        S.user.email = $('in-email').value.trim();
        save();
    }

    function applyEmail() {
        const box = $('email-suggest');
        $('in-email').value = box.dataset.value;
        box.hidden = true;
        onEmailInput();
    }

    // Acepta "+57 310 123 4567" pegado desde los contactos y lo deja en 10 dígitos
    function onPhone(input) {
        let v = input.value.replace(/\D/g, '');
        if (v.length > 10 && v.startsWith('57')) v = v.slice(2);
        v = v.slice(0, 10);
        if (v !== input.value) input.value = v;
        S.user.phone = v;
        save();
    }

    function submitContacto(e) {
        e.preventDefault();
        const email = $('in-email').value.trim();
        // Si el correo parece mal escrito, lo mostramos una vez antes de seguir
        if (emailSuggestShownFor !== email && checkEmail()) {
            $('email-suggest').scrollIntoView({ block: 'center', behavior: 'smooth' });
            return;
        }
        S.user.email = email;
        S.user.phone = $('in-phone').value;
        S.consent = {
            aceptado: true,
            fecha: new Date().toLocaleString('es-CO', { timeZone: 'America/Bogota' }),
            texto: 'Autorizo el tratamiento de mis datos para emitir mi certificado y contactarme sobre este proceso (Ley 1581 de 2012).'
        };
        save();
        trackEvent('registration_submitted', { consentimiento_datos: S.consent });
        createCrmLead();
        go('pago');
    }

    // ════════════════ Pago ════════════════
    function payPSE() {
        // El link de PSE no trae monto: copiamos el valor para que solo lo pegue
        copyText(String(C.precio));
        trackCheckout('PSE');
        S.metodo = 'PSE';
        S.pago = 'iniciado';
        go('comprobante');
        // PSE en otra pestaña: esta queda lista para enviar el comprobante al volver.
        // Si el navegador bloquea la pestaña, abrimos PSE aquí mismo (el estado ya quedó guardado).
        const win = window.open(C.pseUrl, '_blank');
        if (!win) window.location.href = C.pseUrl;
    }

    function goTransfer() {
        trackCheckout('Bancolombia');
        S.metodo = 'Bancolombia';
        if (!S.pago) S.pago = 'iniciado';
        go('transferencia');
    }

    function copy(btn, text) {
        copyText(text).then(ok => {
            if (!ok) return;
            btn.innerHTML = '<i class="fas fa-check"></i> ¡Copiado!';
            btn.classList.add('copied');
            setTimeout(() => {
                btn.innerHTML = '<i class="far fa-copy"></i> Copiar';
                btn.classList.remove('copied');
            }, 2000);
        });
    }

    function sendProof(metodo) {
        metodo = metodo || S.metodo || 'PSE';
        trackEvent('whatsapp_comprobante', { metodo: metodo });
        S.metodo = metodo;
        S.pago = 'comprobante_enviado';
        go('listo');

        const u = S.user;
        const msg = (metodo === 'Bancolombia'
                ? '¡Hola! Ya transferí a Bancolombia el pago de mi ' + C.producto.toLowerCase() + ' ✅\n'
                : '¡Hola! Ya pagué por PSE mi ' + C.producto.toLowerCase() + ' ✅\n') +
            'Adjunto el comprobante de pago para su verificación.\n\n' +
            '• Nombre: ' + (u.name || '') + '\n' +
            '• Documento: ' + ((u.type || '') + ' ' + (u.num || '')).trim() + '\n' +
            '• Correo: ' + (u.email || '');
        openWhatsApp(C.whatsapp, msg);
    }

    function reset() {
        if (!confirm('¿Empezar un certificado nuevo? Se borrarán los datos de este.')) return;
        try { localStorage.removeItem(C.storageKey); } catch (e) {}
        S = initialState();
        history.replaceState(null, '');
        render();
    }

    // ════════════════ API para los botones ════════════════
    window.F = {
        startExam, answer, retry,
        onName, onDoc, showDocType, onDocType, submitNombre,
        checkEmail, onEmailInput, applyEmail, onPhone, submitContacto,
        payPSE, goTransfer, copy, sendProof, back, reset
    };

    document.addEventListener('DOMContentLoaded', () => {
        history.replaceState(ATRAS[S.screen] ? { screen: S.screen } : null, '');
        render();
        trackEvent('page_view');
    });
})();
