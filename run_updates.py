import os

def update_landing():
    file_path = 'servicios/landing-manipulacion.html'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update price
    content = content.replace('22.000', '25.000')

    # Add urgency text in Hero
    search_str = '        <a href="#como-funciona" class="btn-outline">¿Cómo funciona? <i class="fas fa-arrow-down"></i></a>\n      </div>'
    replace_str = '        <a href="#como-funciona" class="btn-outline">¿Cómo funciona? <i class="fas fa-arrow-down"></i></a>\n      </div>\n      <p style="font-size: 13px; color: #dc2626; font-weight: 700; margin-top: 12px;"><i class="fas fa-fire"></i> Precio promocional válido por las próximas 24 horas</p>'
    content = content.replace(search_str, replace_str)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def update_app():
    file_path = 'servicios/curso-manipulacion-de-alimentos.html'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Form autocomplete
    content = content.replace('<input type="text" id="user-fullname" required placeholder="Nombres y Apellidos" class="input-pro capitalize" />', 
                              '<input type="text" id="user-fullname" required placeholder="Nombres y Apellidos" class="input-pro capitalize" autocomplete="name" />')
    
    content = content.replace('<input type="email" id="user-email" required placeholder="ejemplo@correo.com" class="input-pro" />',
                              '<input type="email" id="user-email" required placeholder="ejemplo@correo.com" class="input-pro" autocomplete="email" />')

    # WA Button and CSS
    wa_css = '''
        /* WA Float */
        .wa { position: fixed; bottom: 30px; right: 20px; z-index: 150; width: 52px; height: 52px; background: #25D366; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 14px rgba(37,211,102,.4); transition: .2s; text-decoration: none; }
        .wa:hover { transform: scale(1.1); }
        .wa i { color: #fff; font-size: 24px; }
    </style>'''
    content = content.replace('    </style>', wa_css)

    wa_html = '''
    <!-- WA FLOAT -->
    <a href="https://wa.me/573107941580?text=Hola,%20tengo%20una%20pregunta%20sobre%20el%20certificado%20de%20manipulación%20de%20alimentos" target="_blank" class="wa" aria-label="WhatsApp">
        <i class="fab fa-whatsapp"></i>
    </a>
</body>'''
    content = content.replace('</body>', wa_html)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

try:
    update_landing()
    update_app()
    print("Updates applied successfully.")
except Exception as e:
    print(f"Error: {e}")
