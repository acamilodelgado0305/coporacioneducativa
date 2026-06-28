import os

file_path = 'servicios/curso-manipulacion-de-alimentos.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Move the cancel/reset buttons from checkout to registration
cancel_block = '''                    <div class="pt-1 flex items-center justify-center gap-4">
                        <button onclick="showExitModal()" class="text-xs text-slate-400 hover:text-red-500 transition flex items-center gap-1.5 hover:underline">
                            <i class="fas fa-times text-[9px]"></i> Cancelar
                        </button>
                        <span class="text-slate-200 text-xs\">|</span>
                        <button onclick="startNewProcess()" class="text-xs text-slate-400 hover:text-slate-600 transition flex items-center gap-1.5 hover:underline">
                            <i class="fas fa-redo-alt text-[9px]"></i> Iniciar nuevo proceso
                        </button>
                    </div>'''

if cancel_block in content:
    content = content.replace(cancel_block, '')
    
    # insert it at the end of registration form
    reg_btn_block = '''                    <div class="pt-2">
                        <button type="submit" class="btn-submit-main">
                            <span>Continuar</span>
                        </button>
                    </div>'''
    
    new_reg_btn_block = reg_btn_block + '''\n
                    <!-- Botones movidos desde el checkout -->
                    <div class="pt-4 flex items-center justify-center gap-4">
                        <button type="button" onclick="showExitModal()" class="text-xs text-slate-400 hover:text-red-500 transition flex items-center gap-1.5 hover:underline">
                            <i class="fas fa-times text-[9px]"></i> Cancelar
                        </button>
                        <span class="text-slate-200 text-xs">|</span>
                        <button type="button" onclick="startNewProcess()" class="text-xs text-slate-400 hover:text-slate-600 transition flex items-center gap-1.5 hover:underline">
                            <i class="fas fa-redo-alt text-[9px]"></i> Iniciar nuevo proceso
                        </button>
                    </div>'''
    content = content.replace(reg_btn_block, new_reg_btn_block)
else:
    print('Cancel block not found exactly.')

# 2. Add visual certificate lock and update button copy
nequi_btn_text = '<p class="font-extrabold text-sm leading-tight text-slate-800">Pagar con Nequi en línea — $25.000</p>'
if nequi_btn_text in content:
    new_nequi_text = '<p class="font-extrabold text-sm leading-tight text-slate-800">Desbloquear y Descargar Certificado</p>'
    content = content.replace(nequi_btn_text, new_nequi_text)
    
nequi_sub_text = '<p class="text-xs text-[#DA0063] font-bold leading-tight mt-0.5">Aprobación inmediata · RappiPay PSE</p>'
if nequi_sub_text in content:
    new_nequi_sub_text = '<p class="text-[11px] text-[#DA0063] font-bold leading-tight mt-0.5">Pago seguro con Nequi/PSE — $25.000</p>'
    content = content.replace(nequi_sub_text, new_nequi_sub_text)

btn_end = '</button>\n\n                        <p class="pay-secure"><i class="fas fa-lock"></i> Pago 100% seguro · Cifrado SSL · Procesado por Nequi</p>'
if btn_end in content:
    new_btn_end = '</button>\n                        <p class="text-center text-[10.5px] text-slate-500 mt-2.5 font-medium"><i class="fas fa-bolt text-[#FBC13D]"></i> Toma menos de 1 minuto. Entrega instantánea por correo.</p>\n\n                        <p class="pay-secure"><i class="fas fa-lock"></i> Pago 100% seguro · Cifrado SSL · Procesado por Nequi</p>'
    content = content.replace(btn_end, new_btn_end)

pago_principal = '<!-- PAGO PRINCIPAL -->\n                    <div class="pt-2">'
locked_visual = '''<!-- Certificado bloqueado visual -->
                    <div class="relative bg-slate-50 border border-slate-200 rounded-xl p-4 flex flex-col items-center justify-center text-center overflow-hidden mb-2">
                        <div class="absolute inset-0 opacity-40 blur-[1px] pointer-events-none flex flex-col items-center justify-center" style="background-image: repeating-linear-gradient(0deg, transparent, transparent 10px, #e2e8f0 10px, #e2e8f0 11px); background-size: 100% 20px;">
                            <i class="fas fa-certificate text-5xl text-slate-300 mb-2"></i>
                            <div class="w-2/3 h-2 bg-slate-300 rounded mb-2"></div>
                            <div class="w-1/2 h-2 bg-slate-300 rounded"></div>
                        </div>
                        
                        <div class="relative z-10 flex flex-col items-center">
                            <div class="w-10 h-10 bg-white rounded-full shadow flex items-center justify-center mb-2">
                                <i class="fas fa-lock text-[#0158AD] text-lg"></i>
                            </div>
                            <h3 class="text-sm font-black text-slate-800 mb-0.5">¡Tu certificado está listo!</h3>
                            <p class="text-[11px] text-slate-600 font-medium max-w-[250px] leading-snug">Comienza el pago para desbloquear y descargar tu documento oficial en PDF.</p>
                        </div>
                    </div>\n\n                    '''
content = content.replace(pago_principal, locked_visual + pago_principal)


with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Optimizations applied successfully.')
