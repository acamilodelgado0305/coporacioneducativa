# -*- coding: utf-8 -*-
"""Contenido de la guía de estudio de Auxiliar de Bodega y Logística.

Texto con marcado simple de ReportLab: <b>negrita</b>, <i>cursiva</i>.
Solo caracteres de Windows-1252 (el generador lo valida).
"""

GUIA = {
    'key': 'bodega',
    'course': 'Auxiliar de Bodega y Logística',
    'cover_title': 'Auxiliar de Bodega y Logística',
    'subtitle': 'Recepción, almacenamiento, inventarios, picking, despacho y seguridad en la bodega.',
    'keywords': 'auxiliar de bodega, logística, inventarios, picking, PEPS, guía de estudio',
    'chips': ['8 capítulos', 'Repaso con respuestas', 'Edición 2026'],
    'features': [
        ('De la recepción al despacho', 'Todo el recorrido de la mercancía, paso a paso.'),
        ('Práctica y aplicada', 'Ejemplos de Kardex, ubicaciones, fórmulas y listas de chequeo.'),
        ('Prepárate para el examen', '20 preguntas de repaso con sus respuestas.'),
    ],
    'cover_note': 'Esta guía es tuya y es gratis. Úsala para estudiar antes del examen, prepararte para entrevistas '
                  'de trabajo y consultarla en la bodega cada vez que tengas una duda.',
    'how_to': 'Lee un capítulo a la vez. Fíjate en los recuadros de colores: <b>Recuerda</b> (azul) resume lo '
              'esencial, <b>Atención</b> (naranja) señala errores frecuentes y <b>Dato clave</b> (verde) destaca '
              'cifras y fórmulas que debes dominar. Al final encontrarás un repaso de 20 preguntas con respuestas y un glosario.',

    'blocks': [
        # ─────────────────────────────────────────────────────────
        ('chapter', 'La bodega y el rol del auxiliar',
         'La bodega es el corazón de la cadena de abastecimiento: si falla, el cliente no recibe su pedido.'),
        ('h2', '¿Qué es la logística?'),
        ('p', 'La logística es el proceso de planear y controlar el flujo de mercancías y de información desde el '
              'proveedor hasta el cliente final: <b>el producto correcto, en la cantidad correcta, en el lugar correcto, '
              'en el momento correcto y al menor costo posible</b>.'),
        ('flow', ['Proveedor', 'Recepción', 'Almacena-<br/>miento', 'Alistamiento<br/>(picking)', 'Despacho', 'Cliente']),
        ('h2', 'Funciones del auxiliar de bodega'),
        ('bullets', [
            'Recibir, contar y verificar la mercancía que llega.',
            'Ubicar los productos en el lugar asignado.',
            'Alistar los pedidos (picking) y empacarlos (packing).',
            'Despachar y cargar los vehículos.',
            'Participar en los conteos de inventario.',
            'Registrar entradas, salidas y novedades.',
            'Mantener el orden, el aseo y la seguridad de la bodega.',
        ]),
        ('h2', 'Tipos de bodega'),
        ('table', ['Tipo', 'Qué hace'], [
            ['Materias primas', 'Guarda los insumos que se usan en la producción.'],
            ['Producto terminado', 'Guarda los productos listos para la venta.'],
            ['Centro de distribución (CEDI)', 'Recibe de varios proveedores y despacha a tiendas o clientes.'],
            ['Bodega refrigerada', 'Guarda productos que necesitan cadena de frío.'],
            ['Cross-docking', 'Recibe la mercancía y la despacha casi de inmediato, sin almacenarla.'],
        ], [1.3, 2.7]),
        ('h2', 'Lo que buscan las empresas en un auxiliar'),
        ('bullets', [
            'Orden y atención al detalle.',
            'Responsabilidad con los documentos y las firmas.',
            'Trabajo en equipo y buena comunicación.',
            'Compromiso con la seguridad.',
            'Manejo básico de herramientas digitales: lectores de código de barras, hojas de cálculo y sistemas de bodega.',
        ]),

        # ─────────────────────────────────────────────────────────
        ('chapter', 'Recepción de mercancía',
         'Lo que no se verifica al recibir se convierte en un faltante del inventario.'),
        ('h2', 'La recepción en 8 pasos'),
        ('steps', [
            ('Recibe el vehículo', 'Verifica la cita o programación y dirige el vehículo al muelle asignado.'),
            ('Revisa los documentos', 'Compara la orden de compra con la remisión o factura del proveedor.'),
            ('Inspecciona el vehículo y la carga', 'Que esté limpio y seco y que la carga no venga golpeada, mojada o abierta.'),
            ('Descarga con seguridad', 'Usa el equipo adecuado (transpaleta, montacargas operado por personal autorizado) '
                                       'y la técnica correcta de levantamiento.'),
            ('Cuenta y verifica', 'Referencia, cantidad, unidad de empaque, lote, fecha de vencimiento y estado de cada producto.'),
            ('Registra las novedades', 'Anota faltantes, sobrantes, averías o productos vencidos en el documento, antes de firmar.'),
            ('Ingresa al sistema', 'Registra la entrada para que el inventario quede actualizado.'),
            ('Ubica la mercancía', 'Llévala a la ubicación asignada aplicando el método de rotación definido.'),
        ]),
        ('callout', 'warn', 'Nunca firmes una remisión sin verificar',
         'Tu firma significa que recibiste todo completo y en buen estado. Si firmas sin contar, cualquier faltante o '
         'avería pasa a ser una pérdida para la empresa, y es muy difícil reclamarla después al proveedor.'),
        ('h2', 'Novedades más comunes y qué hacer'),
        ('table', ['Novedad', 'Qué hacer'], [
            ['Faltante', 'Registra la cantidad que falta en la remisión y repórtalo a tu jefe y al proveedor.'],
            ['Sobrante', 'No lo ingreses sin autorización; regístralo como novedad.'],
            ['Avería (roto, mojado, golpeado)', 'Sepáralo, tómale una foto, regístralo y no lo ubiques con la mercancía buena.'],
            ['Vencido o próximo a vencer', 'Revisa la política de la empresa; normalmente se rechaza.'],
            ['Referencia equivocada', 'No la recibas como si fuera la correcta; repórtala.'],
        ], [1.3, 2.7]),
        ('h2', 'Documentos de la recepción'),
        ('table', ['Documento', 'Para qué sirve'], [
            ['Orden de compra', 'Lo que la empresa le pidió al proveedor.'],
            ['Remisión', 'Acompaña la mercancía e indica qué se está enviando.'],
            ['Factura', 'Documento de cobro del proveedor.'],
            ['Informe o acta de recepción', 'Registro interno de lo recibido y sus novedades.'],
        ], [1.3, 2.7]),

        # ─────────────────────────────────────────────────────────
        ('chapter', 'Almacenamiento',
         'Un producto bien ubicado se encuentra rápido, no se daña y no se vence en el olvido.'),
        ('h2', 'Ubicaciones codificadas'),
        ('p', 'Cada espacio de la bodega tiene un código único para encontrar cualquier producto sin buscarlo. Una forma '
              'muy usada es <b>pasillo - rack - nivel</b>.'),
        ('rack', 'A', 4, 3, 3, 2),
        ('p', 'La casilla marcada se lee <b>A-03-2</b>: pasillo A, rack 03, nivel 2. Los niveles normalmente se cuentan '
              'desde el piso hacia arriba; confirma siempre la convención de tu bodega.'),
        ('h2', 'Ubicación fija y ubicación aleatoria'),
        ('bullets', [
            '<b>Fija:</b> cada referencia tiene siempre el mismo lugar. Es fácil de aprender, pero desperdicia espacio.',
            '<b>Aleatoria (o caótica):</b> el producto se guarda en cualquier espacio libre y el sistema registra dónde '
            'quedó. Aprovecha mejor el espacio, pero exige registrar cada movimiento con precisión.',
        ]),
        ('h2', 'Clasificación ABC'),
        ('p', 'No todos los productos se mueven igual. En muchas bodegas, un grupo pequeño de referencias concentra la '
              'mayor parte de los movimientos (principio de Pareto o regla 80/20). Por eso los productos de mayor rotación '
              '(<b>A</b>) se ubican cerca de la zona de despacho y en niveles de fácil acceso, y los de menor rotación '
              '(<b>C</b>) más lejos o en niveles altos.'),
        ('h2', 'Reglas de oro para almacenar'),
        ('bullets', [
            'Almacena sobre estibas o en racks, nunca directamente en el piso.',
            'Usa racks y estanterías en buen estado y respeta su capacidad de carga.',
            'En los arrumes, lo más pesado abajo y lo más liviano arriba.',
            'Respeta la altura máxima de apilamiento indicada en la caja.',
            'Deja libres pasillos, salidas de emergencia, extintores, tableros eléctricos y rociadores.',
            'Separa los productos químicos o peligrosos y ten a mano su hoja de seguridad.',
            'Identifica y separa los productos averiados, vencidos o en devolución.',
        ]),
        ('h2', 'Símbolos de manipulación en las cajas'),
        ('table', ['Símbolo', 'Qué significa'], [
            ['Dos flechas hacia arriba', 'Este lado arriba: la caja no se puede voltear ni acostar.'],
            ['Copa', 'Frágil: manipular con cuidado.'],
            ['Paraguas', 'Proteger de la lluvia y la humedad.'],
            ['Cajas apiladas con un número', 'Número máximo de cajas que se pueden apilar.'],
            ['Gancho tachado', 'No usar ganchos para manipular.'],
            ['Termómetro con límites', 'Rango de temperatura permitido para almacenar.'],
        ], [1.5, 2.5]),
        ('h2', 'Métodos de rotación'),
        ('table', ['Método', 'Significado', 'Cuándo se usa'], [
            ['PEPS (FIFO)', 'Primero en entrar, primero en salir.',
             'La mayoría de productos: evita que la mercancía envejezca en la bodega.'],
            ['FEFO (PVPS)', 'Primero en vencer, primero en salir.',
             'Alimentos, medicamentos, cosméticos y todo producto con fecha de vencimiento.'],
            ['UEPS (LIFO)', 'Último en entrar, primero en salir.',
             'Productos que no se deterioran, como materiales a granel (arena, gravilla).'],
        ], [1, 1.5, 2]),
        ('callout', 'key', 'Ejemplo de PEPS',
         'Tienes tres estibas del mismo producto que ingresaron el 5 de marzo, el 18 de marzo y el 2 de abril. Con PEPS, '
         'la primera que sale es la del 5 de marzo. Si el producto tiene fecha de vencimiento, manda la fecha de '
         'vencimiento más próxima (FEFO).'),
        ('h2', 'Orden y aseo: las 5S'),
        ('table', ['S', 'Qué significa'], [
            ['Seiri', 'Clasificar: retira lo que no sirve.'],
            ['Seiton', 'Ordenar: un lugar para cada cosa y cada cosa en su lugar.'],
            ['Seiso', 'Limpiar: limpia y, al hacerlo, detecta problemas.'],
            ['Seiketsu', 'Estandarizar: define normas para mantener el orden.'],
            ['Shitsuke', 'Disciplina: convierte las 5S en un hábito.'],
        ], [1, 3]),

        # ─────────────────────────────────────────────────────────
        ('chapter', 'Inventarios',
         'El inventario es dinero guardado en forma de productos: cada diferencia es una pérdida o un error que hay que explicar.'),
        ('h2', 'Tipos de conteo'),
        ('table', ['Tipo', 'Cómo se hace', 'Ventaja'], [
            ['Inventario general (físico)', 'Se cuenta toda la bodega, normalmente una o dos veces al año y con la '
                                            'operación detenida.', 'Da una foto completa del inventario.'],
            ['Conteo cíclico', 'Se cuentan referencias específicas de forma periódica (por ejemplo, cada semana) sin '
                               'detener la operación.', 'Detecta errores a tiempo y mantiene el inventario confiable todo el año.'],
            ['Conteo selectivo', 'Se cuentan referencias escogidas al azar o con diferencias sospechosas.',
             'Sirve para verificar o auditar.'],
        ], [1.2, 2, 1.6]),
        ('h2', 'El Kardex'),
        ('p', 'Es el registro de <b>entradas, salidas y saldo</b> de cada referencia. Permite saber cuánto debería haber '
              'en la bodega en todo momento. Ejemplo para una referencia:'),
        ('table', ['Fecha', 'Documento', 'Entrada', 'Salida', 'Saldo'], [
            ['01-mar', 'Saldo inicial', '', '', '120'],
            ['03-mar', 'Recepción OC-1450', '80', '', '200'],
            ['05-mar', 'Despacho R-3321', '', '45', '155'],
            ['08-mar', 'Despacho R-3340', '', '30', '125'],
            ['10-mar', 'Devolución de cliente', '5', '', '130'],
        ], [0.8, 1.8, 0.8, 0.8, 0.8]),
        ('p', 'Si el 10 de marzo el conteo físico da 127 unidades, hay un <b>faltante de 3 unidades</b> que se debe '
              'investigar y registrar como ajuste.'),
        ('h2', 'Faltantes y sobrantes'),
        ('bullets', [
            '<b>Faltante:</b> el conteo físico es menor que el saldo del sistema.',
            '<b>Sobrante:</b> el conteo físico es mayor que el saldo del sistema.',
            '<b>Causas comunes:</b> errores al contar en la recepción o el despacho, documentos sin registrar, averías no '
            'reportadas, productos mal ubicados, errores de digitación, pérdidas o hurtos.',
        ]),
        ('h2', 'Cómo hacer un buen conteo'),
        ('steps', [
            ('Prepara', 'Ordena la zona y ten la lista de referencias y ubicaciones a contar.'),
            ('Congela', 'No muevas mercancía de la zona mientras se cuenta.'),
            ('Cuenta por unidad de manejo', 'Cajas completas × unidades por caja + unidades sueltas.'),
            ('Marca lo contado', 'Así no lo cuentas dos veces ni dejas nada por fuera.'),
            ('Reconfirma', 'Haz un segundo conteo cuando haya diferencias.'),
            ('Registra y reporta', 'Anota el resultado y las novedades. El ajuste lo autoriza el responsable.'),
        ]),
        ('h2', 'Exactitud del inventario'),
        ('formula', 'Exactitud (%) = referencias sin diferencia ÷ referencias contadas × 100', [
            'Ejemplo: contaste 200 referencias y 190 coincidieron con el sistema.',
            '190 ÷ 200 × 100 = <b>95 %</b> de exactitud.',
        ]),

        # ─────────────────────────────────────────────────────────
        ('chapter', 'Picking y packing',
         'El alistamiento es donde más errores se cometen... y donde el cliente los nota.'),
        ('h2', '¿Qué es el picking?'),
        ('p', 'Es el proceso de recoger de sus ubicaciones los productos de un pedido, en la referencia y la cantidad '
              'exactas. Suele ser la actividad que más tiempo y mano de obra consume en una bodega.'),
        ('h2', 'Métodos de picking'),
        ('table', ['Método', 'Cómo funciona'], [
            ['Por pedido', 'Se alista un pedido completo a la vez. Es simple y con pocos errores.'],
            ['Por lotes', 'Se recogen juntos los productos de varios pedidos y luego se separan. Ahorra recorridos.'],
            ['Por zonas', 'Cada auxiliar alista solo los productos de su zona.'],
            ['Por oleadas', 'Se agrupan los pedidos por horario o por ruta de despacho.'],
        ], [1, 3]),
        ('h2', 'Herramientas'),
        ('bullets', [
            'Orden o lista de alistamiento (picking list), en papel o en pantalla.',
            'Lector de código de barras o terminal de radiofrecuencia (RF).',
            'Sistemas de luces (pick to light) o de voz (pick by voice) en bodegas automatizadas.',
        ]),
        ('h2', 'Buenas prácticas de picking'),
        ('bullets', [
            'Verifica referencia, presentación y cantidad antes de tomar el producto.',
            'Aplica la rotación (PEPS o FEFO) también al alistar.',
            'Sigue la ruta más corta y evita devolverte por el mismo pasillo.',
            'Si encuentras un producto averiado, sepáralo y repórtalo como novedad: nunca lo despaches.',
            'Si no hay existencia suficiente, repórtalo; no lo reemplaces por otra referencia sin autorización.',
        ]),
        ('h2', 'Packing (empaque)'),
        ('steps', [
            ('Elige el empaque', 'Adecuado al tamaño, el peso y la fragilidad del producto.'),
            ('Protege', 'Usa relleno (papel, plástico de burbujas) para que el producto no se mueva.'),
            ('Cierra y sella', 'Que la caja quede firme y no se abra en el transporte.'),
            ('Rotula', 'Destinatario, dirección, número de pedido, número de bulto (por ejemplo, 1 de 3) y símbolos de manipulación.'),
            ('Adjunta la lista de empaque', 'Si se requiere, con el detalle de lo que lleva cada bulto.'),
        ]),

        # ─────────────────────────────────────────────────────────
        ('chapter', 'Despacho y transporte',
         'El último control antes de que el pedido llegue al cliente.'),
        ('h2', 'El despacho en 6 pasos'),
        ('steps', [
            ('Consolida', 'Reúne el pedido completo en la zona de despacho.'),
            ('Verifica', 'Compara referencias y cantidades contra la remisión o factura.'),
            ('Inspecciona el vehículo', 'Limpio, seco, sin olores y con la carrocería o la carpa en buen estado.'),
            ('Carga en orden inverso a la ruta', 'Lo que se entrega de último va al fondo; lo primero, cerca de la puerta.'),
            ('Distribuye y asegura', 'Lo pesado abajo y centrado; asegura la carga para que no se desplace.'),
            ('Entrega documentos y registra', 'Remisión, factura y guía de transporte al conductor; registra la salida.'),
        ]),
        ('callout', 'key', 'Verifica antes de cerrar el vehículo',
         'Corregir un error en la bodega cuesta minutos; corregirlo donde el cliente cuesta un viaje, dinero y la '
         'confianza del cliente.'),
        ('h2', 'Documentos del despacho'),
        ('table', ['Documento', 'Para qué sirve'], [
            ['Remisión', 'Relaciona lo que sale y respalda la entrega.'],
            ['Factura', 'Documento de venta al cliente.'],
            ['Guía de transporte', 'Documento de la transportadora para el envío.'],
            ['Lista de empaque', 'Detalla el contenido de cada bulto.'],
        ], [1.3, 2.7]),
        ('h2', 'Devoluciones (logística inversa)'),
        ('steps', [
            ('Recibe con soporte', 'Toda devolución llega con un documento que la respalda.'),
            ('Verifica', 'Motivo, cantidad y estado del producto.'),
            ('Clasifica', 'Apto para la venta, averiado o vencido.'),
            ('Registra y ubica', 'Ingresa la devolución al sistema y ubícala en la zona que corresponde.'),
        ]),

        # ─────────────────────────────────────────────────────────
        ('chapter', 'Seguridad y salud en el trabajo',
         'Ningún pedido es más urgente que tu integridad.'),
        ('h2', 'Riesgos más comunes en la bodega'),
        ('bullets', [
            'Caída de objetos desde los racks.',
            'Golpes y atrapamientos con mercancía o equipos.',
            'Sobreesfuerzos y lesiones de espalda al levantar cargas.',
            'Caídas al mismo nivel (pisos mojados, desorden) o a distinto nivel (escaleras, plataformas).',
            'Atropellamientos con montacargas o transpaletas.',
            'Incendios.',
        ]),
        ('h2', 'Elementos de protección personal (EPP)'),
        ('table', ['EPP', 'Te protege de'], [
            ['Botas de seguridad con puntera', 'Caída de objetos sobre los pies y aplastamientos.'],
            ['Guantes', 'Cortes, astillas y raspaduras al manipular cajas y estibas.'],
            ['Casco', 'Golpes y caída de objetos desde altura.'],
            ['Chaleco reflectivo', 'Atropellamientos: te hace visible para los operadores de equipos.'],
            ['Gafas o protección auditiva', 'Partículas o ruido excesivo, cuando la tarea lo requiera.'],
        ], [1.5, 2.5]),
        ('h2', 'Levantamiento manual de cargas'),
        ('steps', [
            ('Evalúa la carga', 'Peso, tamaño y si necesitas ayuda o un equipo.'),
            ('Acércate', 'Separa los pies a la altura de los hombros, cerca de la carga.'),
            ('Flexiona las rodillas', 'Y mantén la espalda recta.'),
            ('Agarra firme', 'Y pega la carga al cuerpo.'),
            ('Levanta con las piernas', 'Sin tirones ni movimientos bruscos.'),
            ('No gires el tronco', 'Para cambiar de dirección, mueve los pies.'),
        ]),
        ('callout', 'warn', 'Límites de peso',
         'En Colombia, la Resolución 2400 de 1979 establece como referencia un máximo de 25 kg de carga compacta para '
         'hombres y 12,5 kg para mujeres al levantar cargas manualmente. Si la carga supera tu capacidad, pide ayuda o '
         'usa una ayuda mecánica.'),
        ('h2', 'Equipos de la bodega'),
        ('bullets', [
            '<b>Transpaleta (gato o estibador):</b> úsala empujando, con la carga centrada y sin superar su capacidad.',
            '<b>Montacargas:</b> solo lo opera personal capacitado y autorizado. Como peatón, mantente lejos de su radio '
            'de giro y usa los pasillos peatonales.',
            '<b>Escaleras:</b> revisa su estado antes de usarlas y mantén siempre tres puntos de apoyo.',
            '<b>Trabajo en alturas:</b> en Colombia, las tareas a 2 metros o más de altura requieren capacitación y '
            'certificación específicas (Resolución 4272 de 2021).',
        ]),
        ('h2', 'Emergencias'),
        ('bullets', [
            'Conoce las rutas de evacuación, las salidas y el punto de encuentro.',
            'Nunca bloquees extintores, salidas ni tableros eléctricos.',
            'Reporta de inmediato los incidentes, las condiciones inseguras y los casi accidentes.',
            'Participa en los simulacros.',
        ]),
        ('p', 'Todas las empresas en Colombia deben implementar el Sistema de Gestión de Seguridad y Salud en el Trabajo '
              '(SG-SST), según el Decreto 1072 de 2015. Como trabajador, tu parte es cumplir las normas, usar los EPP y '
              'reportar los riesgos.'),

        # ─────────────────────────────────────────────────────────
        ('chapter', 'Tecnología e indicadores',
         'Lo que se mide se puede mejorar: así se evalúa el trabajo de una bodega.'),
        ('h2', 'Tecnología en la bodega'),
        ('bullets', [
            '<b>Código de barras:</b> identifica cada producto. En Colombia la mayoría de productos usa el estándar GS1 (EAN-13).',
            '<b>Lector o terminal RF:</b> registra entradas, ubicaciones y salidas en tiempo real y reduce los errores de digitación.',
            '<b>WMS (sistema de gestión de bodegas):</b> software que controla ubicaciones, inventarios, picking y despachos.',
            '<b>ERP:</b> sistema de la empresa que integra compras, ventas, inventario y contabilidad.',
        ]),
        ('h2', 'Indicadores clave'),
        ('table', ['Indicador', 'Qué mide', 'Cómo se calcula'], [
            ['Exactitud del inventario', 'Qué tan confiable es el inventario.',
             'Referencias sin diferencia ÷ referencias contadas × 100'],
            ['Pedidos perfectos', 'Pedidos entregados completos, a tiempo y sin errores.',
             'Pedidos perfectos ÷ total de pedidos × 100'],
            ['Tiempo de alistamiento', 'La rapidez del picking.', 'Tiempo total de alistamiento ÷ número de pedidos'],
            ['Rotación de inventario', 'Cuántas veces se renueva el inventario en un periodo.',
             'Costo de lo vendido ÷ inventario promedio'],
            ['Mercancía averiada', 'Las pérdidas por daños.', 'Unidades averiadas ÷ unidades manejadas × 100'],
        ], [1.2, 1.5, 1.8]),
        ('callout', 'info', 'Tu trabajo se refleja en los indicadores',
         'Contar bien en la recepción, ubicar en el sitio correcto y verificar antes de despachar son las acciones que '
         'más mejoran la exactitud del inventario y los pedidos perfectos.'),

        # ─────────────────────────────────────────────────────────
        ('section', 'Repaso: pon a prueba lo que aprendiste', 'repaso',
         'Responde sin mirar y luego compara con las respuestas al final.'),
        ('quiz', [
            ('¿Qué es lo primero que debes hacer al recibir mercancía?',
             ['Ubicarla de inmediato', 'Verificar los documentos contra lo que llegó físicamente', 'Firmar la remisión'], 1),
            ('PEPS (FIFO) significa:', ['Primero en entrar, primero en salir', 'Pedido entregado, pedido salido',
                                        'Primero empacar, primero separar'], 0),
            ('Para alimentos y medicamentos normalmente se usa:',
             ['UEPS', 'FEFO: primero en vencer, primero en salir', 'Ubicación aleatoria'], 1),
            ('La ubicación B-02-3 se lee:', ['Pasillo B, rack 02, nivel 3', 'Nivel B, pasillo 02, rack 3',
                                             'Rack B, nivel 02, pasillo 3'], 0),
            ('En un arrume, la caja más pesada va:', ['Arriba', 'Abajo', 'En el medio'], 1),
            ('El conteo cíclico consiste en:', ['Contar toda la bodega una vez al año',
                                                'Contar referencias específicas de forma periódica',
                                                'Contar solo lo que se despacha'], 1),
            ('Si el sistema dice 50 unidades y cuentas 47, tienes:',
             ['Un sobrante de 3', 'Un faltante de 3', 'Un inventario exacto'], 1),
            ('El Kardex registra:', ['Entradas, salidas y saldo de cada referencia', 'Los horarios del personal',
                                     'Las rutas de los camiones'], 0),
            ('El picking es:', ['Recoger y alistar los productos de un pedido', 'Barrer los pasillos', 'Cargar el camión'], 0),
            ('Si durante el alistamiento encuentras un producto averiado:',
             ['Lo despachas igual', 'Lo separas y lo reportas como novedad', 'Lo guardas al fondo del rack'], 1),
            ('Al cargar un vehículo con varias entregas:',
             ['Lo que se entrega de último va al fondo', 'Lo que se entrega primero va al fondo', 'Se carga en cualquier orden'], 0),
            ('¿Qué documento respalda la salida de mercancía?',
             ['La remisión o la factura', 'Una nota en el cuaderno', 'Un mensaje de chat'], 0),
            ('¿Qué EPP protege los pies de la caída de objetos?',
             ['Tenis deportivos', 'Botas de seguridad con puntera', 'Sandalias'], 1),
            ('Para levantar una caja del suelo debes:',
             ['Doblar la espalda con las piernas rectas', 'Flexionar las rodillas con la espalda recta',
              'Girar el tronco mientras levantas'], 1),
            ('¿Quién puede operar un montacargas?',
             ['Cualquier auxiliar', 'Solo personal capacitado y autorizado', 'El conductor del camión'], 1),
            ('La mercancía debe almacenarse:', ['Directamente en el piso', 'Sobre estibas o en racks', 'En los pasillos'], 1),
            ('Una caja con el símbolo de una copa indica que el producto es:', ['Frágil', 'Líquido', 'Una bebida'], 0),
            ('¿Qué significa Seiri, la primera de las 5S?',
             ['Limpiar', 'Clasificar y retirar lo que no sirve', 'Estandarizar'], 1),
            ('Contaste 100 referencias y 96 coincidieron con el sistema. La exactitud del inventario es:',
             ['4 %', '96 %', '100 %'], 1),
            ('Antes de firmar la remisión del proveedor debes:',
             ['Contar, verificar y anotar las novedades', 'Firmar rápido para no demorar al conductor',
              'Pedirle a otro compañero que firme'], 0),
        ]),

        ('section', 'Glosario', 'glosario'),
        ('glossary', [
            ('Arrume', 'pila de cajas o bultos colocados uno sobre otro.'),
            ('Avería', 'daño de un producto (roto, mojado, golpeado) que impide venderlo en condiciones normales.'),
            ('Cross-docking', 'método en el que la mercancía se recibe y se despacha casi de inmediato, sin almacenarla.'),
            ('Estiba', 'plataforma, generalmente de madera o plástico, sobre la que se coloca la mercancía para moverla '
                       'y almacenarla (también llamada pallet).'),
            ('FEFO', 'primero en vencer, primero en salir.'),
            ('Inventario', 'conjunto de mercancías que tiene la empresa en un momento determinado.'),
            ('Kardex', 'registro de entradas, salidas y saldo de cada referencia.'),
            ('Lote', 'grupo de unidades fabricadas en las mismas condiciones, identificado con un código.'),
            ('Muelle', 'zona de la bodega donde los vehículos cargan y descargan.'),
            ('Packing', 'proceso de empacar y rotular un pedido para su despacho.'),
            ('PEPS', 'primero en entrar, primero en salir.'),
            ('Picking', 'alistamiento: recoger de sus ubicaciones los productos de un pedido.'),
            ('Rack', 'estructura metálica de estanterías para almacenar mercancía en altura.'),
            ('Referencia (SKU)', 'código que identifica un producto específico en el inventario.'),
            ('Remisión', 'documento que acompaña la mercancía e indica qué se envía.'),
            ('WMS', 'sistema de gestión de bodegas (Warehouse Management System).'),
        ]),
    ],

    'cta_title': 'Siguiente paso: tu certificado',
    'cta_text': [
        'Ya tienes las bases. Presenta el examen gratis en CertiTec y, al aprobarlo, recibe tu diploma y tu '
        'certificado de Auxiliar de Bodega y Logística para adjuntar a tu hoja de vida.',
    ],
    'cta_bullets': [
        'Diploma y certificado en PDF a tu nombre y número de documento.',
        'Emitidos y firmados por Alianza Capacitarte.',
        'Verificables en línea con tu número de documento.',
        'Soporte personalizado por WhatsApp.',
    ],
}
