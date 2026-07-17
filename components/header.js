/**
 * <site-header> — Header compartido para todas las páginas
 *
 * Atributos opcionales:
 *   course      → subtítulo del curso (ej: "Manipulación de Alimentos")
 *   cta-text    → texto del botón CTA (ej: "Iniciar Examen")
 *   cta-href    → destino del botón CTA (ej: "#examen")
 *   cta-color   → color de fondo del CTA en hex (default: #0158AD)
 *   logo-src    → ruta manual al logo (si no se especifica se detecta automáticamente)
 */
(function () {
  if (!document.getElementById('site-header-base-styles')) {
    const s = document.createElement('style');
    s.id = 'site-header-base-styles';
    s.textContent = `
      site-header { display: block; }
      .sh-root {
        position: sticky;
        top: 0;
        z-index: 50;
        background: rgba(255,255,255,0.97);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-bottom: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px 0 rgba(0,0,0,0.06);
      }
      .sh-inner {
        max-width: 1100px;
        margin: 0 auto;
        padding: 10px 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 12px;
      }
      .sh-brand {
        display: flex;
        align-items: center;
        gap: 10px;
        text-decoration: none;
        flex-shrink: 0;
      }
      .sh-brand img {
        height: 36px;
        width: auto;
      }
      .sh-brand-text {
        line-height: 1;
      }
      .sh-brand-name {
        font-size: 16px;
        font-weight: 800;
        color: #0f172a;
        letter-spacing: -0.02em;
        line-height: 1.1;
      }
      .sh-brand-name span { color: #0158AD; }
      .sh-brand-sub {
        font-size: 9px;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 600;
        margin-top: 2px;
        display: block;
      }
      .sh-right {
        display: flex;
        align-items: center;
        gap: 8px;
      }
      .sh-nav {
        display: none;
        gap: 20px;
        align-items: center;
        margin-right: 8px;
      }
      .sh-nav a {
        font-size: 13px;
        font-weight: 500;
        color: #64748b;
        text-decoration: none;
        transition: color 0.15s;
      }
      .sh-nav a:hover { color: #0f172a; }
      .sh-cta {
        font-size: 11px;
        font-weight: 700;
        color: #fff;
        padding: 8px 16px;
        border-radius: 999px;
        text-decoration: none;
        transition: opacity 0.15s, transform 0.1s;
        white-space: nowrap;
        display: none;
        align-items: center;
        gap: 6px;
        box-shadow: 0 2px 8px -2px rgba(0,0,0,0.18);
      }
      .sh-cta:hover { opacity: 0.88; }
      .sh-cta:active { transform: scale(0.97); }
      .sh-support {
        font-size: 11px;
        font-weight: 700;
        color: #475569;
        border: 1px solid #e2e8f0;
        padding: 7px 13px;
        border-radius: 999px;
        text-decoration: none;
        display: flex;
        align-items: center;
        gap: 6px;
        transition: background 0.15s;
        white-space: nowrap;
        flex-shrink: 0;
      }
      .sh-support:hover { background: #f8fafc; }
      @media (min-width: 640px) {
        .sh-nav  { display: flex; }
        .sh-cta  { display: flex; }
        .sh-brand img { height: 40px; }
        .sh-brand-name { font-size: 17px; }
      }
    `;
    document.head.appendChild(s);
  }

  class SiteHeader extends HTMLElement {
    connectedCallback() {
      const isSubdir = window.location.pathname.replace(/\\/g, '/').includes('/servicios/');
      const base     = isSubdir ? '../' : '';

      const logoSrc  = this.getAttribute('logo-src')  || `${base}logof.png`;
      const course   = this.getAttribute('course')    || '';
      const ctaText  = this.getAttribute('cta-text')  || '';
      const ctaHref  = this.getAttribute('cta-href')  || '#';
      const ctaColor = this.getAttribute('cta-color') || '#0158AD';

      const homeUrl   = `${base}index.html`;
      const cursosUrl = `${base}index.html#cursos`;

      const subHtml = course
        ? `<span class="sh-brand-sub">${course}</span>`
        : `<span class="sh-brand-sub">Formación Virtual</span>`;

      const ctaHtml = ctaText
        ? `<a href="${ctaHref}" class="sh-cta" style="background:${ctaColor}">
             <svg width="11" height="11" viewBox="0 0 24 24" fill="currentColor" style="flex-shrink:0"><path d="M8 5v14l11-7z"/></svg>
             ${ctaText}
           </a>`
        : '';

      this.innerHTML = `
        <div class="sh-root">
          <div class="sh-inner">
            <a href="${homeUrl}" class="sh-brand">
              <img src="${logoSrc}" alt="CertiTec Colombia" onerror="this.style.display='none'">
              <div class="sh-brand-text">
                <div class="sh-brand-name">CertiTec <span>Colombia</span></div>
                ${subHtml}
              </div>
            </a>
            <div class="sh-right">
              <nav class="sh-nav">
                <a href="${homeUrl}">Inicio</a>
                <a href="${cursosUrl}">Cursos</a>
              </nav>
              ${ctaHtml}
              <a href="https://wa.me/573107941580" target="_blank" rel="noopener" class="sh-support">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="#25D366" style="flex-shrink:0">
                  <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
                </svg>
                Soporte
              </a>
            </div>
          </div>
        </div>`;
    }
  }

  if (!customElements.get('site-header')) {
    customElements.define('site-header', SiteHeader);
  }
})();
