/**
 * Flujo de venta de certificados — una sola decisión por pantalla.
 *
 *   inicio → examen → (fallo) → datos → pedido → listo
 *
 * Cada curso es una página que define `window.CURSO` (precio, preguntas, textos)
 * y carga este archivo. Ver certificado-manipulacion-de-alimentos.html.
 *
 * Integraciones (las mismas de las páginas anteriores):
 *   - n8n (Telegram): trackEvent()
 *   - CRM: createCrmLead() al completar los datos (y de nuevo al confirmar el pedido, si falló)
 *          y markLeadAsProposal() al confirmar el pedido
 *   - Meta: Pixel 'Lead' (con event_id compartido con la CAPI del CRM) e 'InitiateCheckout'
 *   - Pago: si el curso define `nequiUrl`, se paga con Nequi en ese link de Wompi; la
 *           pasarela confirma el pago, sin comprobante. Con `pagoEnLinea` el botón es
 *           "Pagar" (azul, con los logos de los medios) en vez de la tarjeta de Nequi, para links de Wompi que
 *           aceptan todos los medios. Si el link no trae el valor, se copia al portapapeles
 *           (con `valorEnLink` ya viene puesto). Si no hay link, o si el cliente lo prefiere,
 *           "Confirmar pedido" abre el chat con los datos y allí se coordina el pago.
 */
(function () {
    const C = window.CURSO;

    const N8N_WEBHOOK     = 'https://n8n.certitecol.com/webhook/6a03322d-f85e-46df-a0f4-fb27010a6b0c';
    const CRM_LEADS_URL   = 'https://controla-570877385695.northamerica-northeast1.run.app/api/crm/leads/publico';
    const CRM_BUSINESS_ID = 3;

    const PRECIO_TXT = C.precio.toLocaleString('es-CO');   // "25.000", sin el signo $
    const TOTAL      = C.preguntas.length;
    const MIN_OK     = Math.ceil(TOTAL * C.minAprobar);
    const IS_MOBILE  = /Android|iPhone|iPad|iPod|Opera Mini|IEMobile/i.test(navigator.userAgent);
    // El mismo logo del botón "Pagar con Nequi" del checkout anterior.
    // Se carga sin referrer: con el de la página Google a veces lo bloquea (429).
    const NEQUI_LOGO = 'https://yt3.googleusercontent.com/tBl_djxQMQ-IAxboBoNRIeKJ9hDXG8fC-M2ZEWHWCykr-P0umEveM3dbGi4Di04EHFRn7aB7=s900-c-k-c0x00ffffff-no-rj';
    // Botón azul "Pagar" (Nequi, PSE o tarjeta en Wompi) en lugar de la tarjeta de Nequi
    const EN_LINEA = !!(C.nequiUrl && C.pagoEnLinea);
    // Debajo de ese botón: los medios que acepta Wompi y el respaldo de Bancolombia
    const PAGO_SEGURO = `
                <div class="pay-trust">
                    <span class="pay-logos" role="img" aria-label="Nequi, PSE, Visa y Mastercard">
                        <span class="nequi"><img src="${NEQUI_LOGO}" alt="" width="18" height="18" referrerpolicy="no-referrer" onerror="this.remove()">Nequi</span>
                        <span class="pse">PSE</span>
                        <span class="visa">VISA</span>
                        <span><svg viewBox="0 0 30 18" width="24" height="15" aria-hidden="true"><circle cx="10" cy="9" r="8" fill="#EB001B"/><circle cx="20" cy="9" r="8" fill="#F79E1B"/><path d="M15 2.8a8 8 0 0 1 0 12.4a8 8 0 0 1 0-12.4z" fill="#FF5F00"/></svg></span>
                    </span>
                    <span class="pay-secure"><i class="fas fa-shield-halved"></i> Pago seguro con Wompi, de Bancolombia</span>
                </div>`;

    // Paso de la barra de progreso y a dónde lleva "Atrás"
    const PASO  = { inicio: 0, examen: 1, fallo: 1, datos: 2, pedido: 3, listo: 4 };
    const ATRAS = { pedido: 'datos' };
    const NOMBRE_PASO = ['', 'Examen', 'Tus datos', C.nequiUrl ? 'Pago' : 'Confirmar', 'Listo'];

    // Etiquetas cortas: el tipo de documento va en la misma fila del número
    const DOCS = {
        CC:  'CC',
        TI:  'TI',
        CE:  'CE',
        PPT: 'PPT',
        PAS: 'Pasaporte'
    };

    // ════════════════ Estado ════════════════
    function initialState() {
        return {
            screen: 'inicio',
            quiz: { idx: 0, score: 0, res: [] },   // res: aciertos por pregunta (true/false)
            user: { type: 'CC', num: '', name: '', phone: '', email: '' },
            consent: null,
            leadCreated: false,
            leadId: null,
            leadProposed: false,
            leadEventId: null,
            pedido: false,     // true al confirmar el pedido o empezar a pagar
            metodo: null       // 'Nequi' | 'WhatsApp'
        };
    }

    let S = loadState();

    function loadState() {
        let saved = null;
        try { saved = JSON.parse(localStorage.getItem(C.storageKey)); } catch (e) {}
        if (!saved) saved = migrateLegacy();
        const s = Object.assign(initialState(), saved || {});
        s.user = Object.assign(initialState().user, s.user || {});
        // Antes los datos se pedían en dos pantallas (nombre y contacto)
        if (s.screen === 'nombre' || s.screen === 'contacto') s.screen = 'datos';
        // Pedidos confirmados antes de que existiera el pago con Nequi
        if (s.pedido && !s.metodo) s.metodo = 'WhatsApp';
        // Pantallas de pago de versiones anteriores (PSE, transferencia, comprobante)
        if (s.screen === 'comprobante' && C.nequiUrl && s.metodo === 'Nequi') s.screen = 'listo';
        if (s.screen === 'pago' || s.screen === 'transferencia' || s.screen === 'comprobante') s.screen = 'pedido';
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
        s.pedido = !!old.psePago;
        s.quiz = { idx: C.preguntas.length, score: (old.quiz && old.quiz.score) || 0 };

        if (old.view === 'view-checkout' && u.name && u.email) {
            s.screen = old.psePago === 'comprobante_enviado' ? 'listo' : 'pedido';
        } else if (old.view === 'view-registration') {
            s.screen = 'datos';
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
    let crmLead = null;   // POST en curso

    // Crea el lead una sola vez; si el intento anterior falló, lo reintenta.
    // Devuelve una promesa que se resuelve cuando el CRM responde (bien o mal),
    // para que el pedido por WhatsApp pueda esperarla.
    function createCrmLead() {
        if (S.leadCreated) return Promise.resolve();
        if (crmLead) return crmLead;
        const u = S.user;
        crmLead = fetch(CRM_LEADS_URL, {
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
            // Si ya confirmó el pedido mientras el CRM respondía, avanzamos el lead ahora
            if (S.pedido) markLeadAsProposal();
        })
        .catch(err => trackEvent('crm_lead_error', { detalle: String((err && err.message) || err) }))
        .finally(() => { crmLead = null; });
        return crmLead;
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
    const VIEWS = {
        inicio: () => `
            <section class="screen">
                ${C.portada ? `
                <figure class="hero">
                    <img src="${C.portada.src}" alt="${C.portada.alt}" width="1100" height="619" fetchpriority="high">
                    <figcaption class="hero-tag"><i class="fas fa-shield-halved"></i> ${C.aval}</figcaption>
                </figure>` : `
                <span class="pill"><i class="fas fa-shield-halved"></i> ${C.aval}</span>`}
                <h1 class="h1">Tu certificado de <span>${C.titulo || C.nombre}</span>, hoy mismo</h1>
                <p class="lead">Todo desde tu celular, sin filas ni papeleo.</p>
                <div class="how">
                    <p class="how-title">Así de fácil</p>
                    <ol>
                        <li><span class="how-n">1</span><div><b>Presenta el examen gratis</b><span>${TOTAL} preguntas · ${C.minutos} minutos · sin registrarte</span></div></li>
                        <li><span class="how-n">2</span><div><b>Pagas solo si apruebas</b><span>${PRECIO_TXT} · ${EN_LINEA ? 'pagas en línea con Nequi, PSE o tarjeta' : C.nequiUrl ? 'pagas con Nequi en línea' : 'coordinamos el pago por WhatsApp'}</span></div></li>
                        <li><span class="how-n">3</span><div><b>Recibe ${C.entrega}</b><span>En PDF, en tu correo el mismo día</span></div></li>
                    </ol>
                </div>
            </section>
            <div class="actions">
                <button class="btn btn-primary" onclick="F.startExam()">Empezar examen gratis <i class="fas fa-arrow-right"></i></button>
                <p class="fine"><i class="fas fa-shield-halved"></i> Certificado verificable en línea · <a href="../verificacion.html" target="_blank">Verificar uno</a></p>
            </div>`,

        examen: () => {
            const q = C.preguntas[S.quiz.idx];
            const res = S.quiz.res || [];
            let racha = 0;
            for (let k = res.length - 1; k >= 0 && res[k]; k--) racha++;
            return `
            <section class="screen">
                <div class="q-head">
                    <p class="q-count">Pregunta ${S.quiz.idx + 1} de ${TOTAL}</p>
                    ${racha >= 2 ? `<span class="q-streak"><i class="fas fa-fire"></i> ${racha} seguidas</span>` : ''}
                </div>
                <div class="q-dots" aria-hidden="true">${C.preguntas.map((_, k) =>
                    `<i class="${k < res.length ? (res[k] ? 'ok' : 'bad') : k === S.quiz.idx ? 'now' : ''}"></i>`).join('')}</div>
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

        datos: () => `
            <section class="screen">
                <div class="success-banner">
                    <i class="fas fa-circle-check"></i>
                    <div><b>¡Aprobaste con ${S.quiz.score}/${TOTAL}!</b><span>Completa tus datos para emitir ${C.entrega}</span></div>
                </div>
                <form id="f-datos" class="form" onsubmit="F.submitDatos(event)">
                    <label class="field">
                        <span class="label">Nombre completo</span>
                        <input id="in-name" class="input" required autocomplete="name" autocapitalize="words"
                               placeholder="Nombres y apellidos" value="${esc(S.user.name)}" oninput="F.onName(this)">
                        <span class="hint">Así aparecerá en tu certificado</span>
                    </label>
                    <div class="field">
                        <label class="label" for="in-doc">Tipo y número de documento</label>
                        <div class="doc-row">
                            <select id="in-doctype" class="input${S.user.type === 'PAS' ? ' wide' : ''}" aria-label="Tipo de documento" onchange="F.onDocType(this)">
                                ${Object.keys(DOCS).map(k => `<option value="${k}" ${S.user.type === k ? 'selected' : ''}>${DOCS[k]}</option>`).join('')}
                            </select>
                            <input id="in-doc" class="input" required autocomplete="off" maxlength="20" placeholder="Sin puntos"
                                   value="${esc(S.user.num)}" oninput="F.onDoc(this)">
                        </div>
                    </div>
                    <div class="field">
                        <label class="label" for="in-email">Correo electrónico</label>
                        <input id="in-email" class="input" type="email" required autocomplete="email" inputmode="email"
                               autocapitalize="off" spellcheck="false" placeholder="tucorreo@gmail.com"
                               value="${esc(S.user.email)}" onblur="F.checkEmail()" oninput="F.onEmailInput()">
                        <button type="button" id="email-suggest" class="email-suggest" hidden onclick="F.applyEmail()"></button>
                        <p class="hint">Aquí te llega ${C.entrega} en PDF</p>
                    </div>
                    <div class="field">
                        <label class="label" for="in-phone">Celular con WhatsApp</label>
                        <span class="input-group">
                            <span class="prefix"><i class="fab fa-whatsapp"></i> +57</span>
                            <input id="in-phone" class="input" type="tel" required inputmode="numeric" autocomplete="tel-national"
                                   pattern="3[0-9]{9}" title="Celular de 10 dígitos que empieza por 3"
                                   placeholder="310 123 4567" value="${esc(S.user.phone)}" oninput="F.onPhone(this)">
                        </span>
                    </div>
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
                <button class="btn btn-primary" type="submit" form="f-datos">Continuar <i class="fas fa-arrow-right"></i></button>
                <p class="fine"><i class="fas fa-lock"></i> Tus datos están protegidos</p>
            </div>`,

        pedido: () => `
            <section class="screen">
                <button class="back" onclick="F.back()"><i class="fas fa-arrow-left"></i> Atrás</button>
                <h1 class="h2">Confirma tu pedido</h1>
                <p class="sub">Revisa que tus datos estén bien: así saldrán en ${C.entrega}.</p>
                <div class="summary">
                    <div class="row"><span>Producto</span><span class="row-val"><b>${C.producto}</b></span></div>
                    <div class="row"><span>A nombre de</span><span class="row-val"><b>${esc(S.user.name)}</b></span></div>
                    <div class="row"><span>Documento</span><span class="row-val"><b>${esc(S.user.type + ' ' + S.user.num)}</b></span></div>
                    <div class="row">
                        <span>Envío a</span>
                        <span class="row-val"><b>${esc(S.user.email)}</b><button class="link" onclick="F.back()">Cambiar</button></span>
                    </div>
                    <div class="row total"><span>Total</span><span class="price">${PRECIO_TXT} <small>COP</small></span></div>
                </div>
                ${C.nequiUrl ? `
                <div class="how">
                    <p class="how-title">Cómo sigue</p>
                    <ol>
                        <li><span class="how-n">1</span><div><b>${EN_LINEA ? 'Paga en línea' : 'Paga con Nequi'}</b><span>${EN_LINEA ? 'Con Nequi, PSE o tarjeta en la página segura de Wompi' : 'Se abre la página de pago segura de Wompi'}</span></div></li>
                        <li><span class="how-n">2</span><div><b>Recibe ${C.entrega}</b><span>En PDF, en tu correo, apenas se apruebe tu pago</span></div></li>
                    </ol>
                </div>
                ${C.valorEnLink ? '' : `
                <p class="note"><i class="fas fa-circle-info"></i><span>Al tocar el botón copiamos el valor <b>${PRECIO_TXT}</b>: pégalo en «¿Cuánto vas a pagar?» y elige ${EN_LINEA ? 'cómo quieres pagar' : '<b>Nequi</b>'}.</span></p>`}
                <button class="btn-link reset-link" onclick="F.reset()">Iniciar un nuevo proceso</button>
            </section>
            <div class="actions">
                ${EN_LINEA ? `
                <button class="btn btn-online" onclick="F.pagarNequi()">Pagar</button>
                ${PAGO_SEGURO}` : `
                <button class="btn-nequi" onclick="F.pagarNequi()">
                    <span class="badge-rec">Recomendado</span>
                    <img src="${NEQUI_LOGO}" alt="Nequi" width="40" height="40" referrerpolicy="no-referrer" onerror="this.remove()">
                    <span class="btn-nequi-txt"><b>Pagar con Nequi en línea — ${PRECIO_TXT}</b><span>Aprobación inmediata</span></span>
                    <i class="fas fa-arrow-right"></i>
                </button>`}
                <button class="btn-link" onclick="F.confirmar()">Prefiero pagar por WhatsApp</button>
            </div>` : `
                <div class="how">
                    <p class="how-title">Cómo sigue</p>
                    <ol>
                        <li><span class="how-n">1</span><div><b>Confirma tu pedido</b><span>Se abre WhatsApp con tus datos listos para enviar</span></div></li>
                        <li><span class="how-n">2</span><div><b>Realiza el pago</b><span>Por el chat te damos las opciones de pago</span></div></li>
                        <li><span class="how-n">3</span><div><b>Envía tu comprobante</b><span>Y te llega ${C.entrega} en PDF a tu correo</span></div></li>
                    </ol>
                </div>
            </section>
            <div class="actions">
                <button class="btn btn-wa" onclick="F.confirmar()"><i class="fab fa-whatsapp"></i> Confirmar pedido</button>
                <button class="btn-link" onclick="F.reset()">Iniciar un nuevo proceso</button>
            </div>`}`,

        listo: () => S.metodo === 'Nequi' ? `
            <section class="screen center">
                <div class="result-icon ok"><i class="fas fa-check"></i></div>
                <h1 class="h2">¡Ya casi, ${esc(firstName())}!</h1>
                <p class="lead">Completa tu pago ${EN_LINEA ? '' : 'con Nequi '}en la página de Wompi. Apenas se apruebe, te enviamos ${C.entrega} en PDF a <b>${esc(S.user.email)}</b>.</p>
                <p class="note"><i class="fas fa-circle-info"></i><span>¿Se cerró la página de pago? Ábrela de nuevo con el botón de abajo. El valor a pagar es <b>${PRECIO_TXT}</b>.</span></p>
            </section>
            <div class="actions">
                <button class="btn btn-outline ${EN_LINEA ? 'online' : 'nequi'}" onclick="F.pagarNequi()"><i class="fas fa-rotate-right"></i> Abrir el pago ${EN_LINEA ? '' : 'con Nequi '}otra vez</button>
                <button class="btn-link" onclick="F.reset()">Hacer otro certificado</button>
            </div>` : `
            <section class="screen center">
                <div class="result-icon ok"><i class="fas fa-check"></i></div>
                <h1 class="h2">¡Pedido confirmado, ${esc(firstName())}!</h1>
                <p class="lead">Envía el mensaje que te dejamos listo en WhatsApp. Allí te damos las opciones de pago y, cuando nos mandes tu comprobante, te enviamos ${C.entrega} en PDF a <b>${esc(S.user.email)}</b>.</p>
                <div class="info-card">
                    <i class="fab fa-whatsapp"></i>
                    <span>¿No se abrió WhatsApp o no alcanzaste a enviar el mensaje? Toca el botón para abrirlo de nuevo.</span>
                </div>
            </section>
            <div class="actions">
                <button class="btn btn-outline" onclick="F.abrirWhatsApp()"><i class="fab fa-whatsapp"></i> Abrir WhatsApp de nuevo</button>
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
        if (S.screen === 'datos') setupDocInput();
        window.scrollTo(0, 0);
    }

    // ════════════════ Examen ════════════════
    function startExam() {
        trackEvent('exam_started');
        S.quiz = { idx: 0, score: 0, res: [] };
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
        (S.quiz.res = S.quiz.res || [])[S.quiz.idx] = correct;
        S.quiz.idx++;
        const dot = document.querySelectorAll('.q-dots i')[S.quiz.idx - 1];
        if (dot) dot.className = correct ? 'ok' : 'bad';
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
            go('datos');
        } else {
            trackEvent('quiz_failed', { score: S.quiz.score + '/' + TOTAL });
            go('fallo');
        }
    }

    function retry() {
        S.quiz = { idx: 0, score: 0, res: [] };
        go('examen');
    }

    // ════════════════ Datos ════════════════
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
    }

    function onDoc(input) {
        const clean = sanitizeDoc(input.value, S.user.type);
        if (clean !== input.value) input.value = clean;
        S.user.num = clean;
        save();
    }

    function onDocType(select) {
        S.user.type = select.value;
        select.classList.toggle('wide', S.user.type === 'PAS');   // "Pasaporte" no cabe en el ancho de "CC"
        setupDocInput();
        onDoc($('in-doc'));
    }

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

    function submitDatos(e) {
        e.preventDefault();
        const email = $('in-email').value.trim();
        // Si el correo parece mal escrito, lo mostramos una vez antes de seguir
        if (emailSuggestShownFor !== email && checkEmail()) {
            $('email-suggest').scrollIntoView({ block: 'center', behavior: 'smooth' });
            return;
        }
        S.user.name = toTitleCase($('in-name').value);
        S.user.num = sanitizeDoc($('in-doc').value, S.user.type);
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
        go('pedido');
    }

    // ════════════════ Pedido ════════════════
    // Con Nequi: paga en el link de Wompi y la pasarela confirma el pago.
    // Por WhatsApp: el pedido llega con todos los datos; allí se le dan las
    // opciones de pago y se recibe el comprobante.
    function pedidoMsg() {
        const u = S.user;
        return '¡Hola! Quiero confirmar mi pedido ✅\n\n' +
            '• Producto: ' + C.producto + '\n' +
            '• Valor: ' + PRECIO_TXT + '\n' +
            '• Nombre: ' + (u.name || '') + '\n' +
            '• Documento: ' + ((u.type || '') + ' ' + (u.num || '')).trim() + '\n' +
            '• Correo: ' + (u.email || '') + '\n' +
            '• Celular: ' + (u.phone || '') + '\n\n' +
            '¿Cómo hago el pago?';
    }

    // Un solo InitiateCheckout por pedido, aunque cambie de método
    function iniciarPedido(metodo) {
        if (!S.pedido) {
            fbqSafe('track', 'InitiateCheckout', { content_name: C.producto, value: C.precio, currency: 'COP', num_items: 1 });
            S.pedido = true;
        }
        S.metodo = metodo;
        markLeadAsProposal();
    }

    function pagarNequi() {
        // Si el link de Wompi no trae el valor, lo copiamos para que solo lo pegue
        if (!C.valorEnLink) copyText(String(C.precio));
        // Aviso de intento de pago a Telegram (n8n) en cada intento, como en el checkout anterior
        // (`boton` distingue la prueba del botón "Pagar en línea")
        trackEvent('payment_initiated', { metodo: 'Nequi', boton: EN_LINEA ? 'Pagar en línea' : 'Nequi' });
        iniciarPedido('Nequi');
        createCrmLead();   // reintento si falló al enviar los datos: la confirmación del pago busca el lead
        go('listo');
        // Wompi en otra pestaña: esta queda en "listo" por si necesita abrir el pago otra vez.
        // Si el navegador bloquea la pestaña, abrimos Wompi aquí mismo (el estado ya quedó guardado).
        const win = window.open(C.nequiUrl, '_blank');
        if (!win) window.location.href = C.nequiUrl;
    }

    let waPendiente = null;   // apertura de WhatsApp que espera al CRM

    function confirmar() {
        if (S.metodo !== 'WhatsApp') trackEvent('pedido_confirmado', { canal: 'WhatsApp' });
        iniciarPedido('WhatsApp');
        go('listo');
        const lead = createCrmLead();   // reintento si falló al enviar los datos
        if (!IS_MOBILE || S.leadCreated) return abrirWhatsApp();
        // En el celular WhatsApp saca al cliente del navegador y la página queda congelada
        // o se cierra: si el CRM aún no respondía, el lead no se registraba ni pasaba a
        // PROPUESTA. Abrimos el chat cuando el CRM responde, máximo 3 s después.
        const turno = waPendiente = {};
        Promise.race([lead, new Promise(r => setTimeout(r, 3000))])
            .then(() => { if (waPendiente === turno) abrirWhatsApp(); });
    }

    function abrirWhatsApp() {
        waPendiente = null;
        openWhatsApp(C.whatsapp, pedidoMsg());
    }

    function reset() {
        if (!confirm('¿Empezar un certificado nuevo? Se borrarán los datos de este.')) return;
        try { localStorage.removeItem(C.storageKey); } catch (e) {}
        waPendiente = null;
        S = initialState();
        history.replaceState(null, '');
        render();
    }

    // ════════════════ API para los botones ════════════════
    window.F = {
        startExam, answer, retry,
        onName, onDoc, onDocType,
        checkEmail, onEmailInput, applyEmail, onPhone, submitDatos,
        pagarNequi, confirmar, abrirWhatsApp, back, reset
    };

    document.addEventListener('DOMContentLoaded', () => {
        // Si la página abre en una pantalla con "Atrás" (p. ej. al volver otro día), se
        // recrea debajo la entrada del paso anterior: si no, "Atrás"/"Cambiar" hacían
        // history.back() y sacaban al usuario de la página.
        history.replaceState(null, '');
        if (ATRAS[S.screen]) history.pushState({ screen: S.screen }, '');
        render();
        trackEvent('page_view');
    });
})();
