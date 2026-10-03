# -*- coding: utf-8 -*-
"""Contenido de la guía de estudio de Manipulación de Alimentos.

Los 8 capítulos siguen el mismo programa que aparece en el certificado que emite
Alianza Capacitarte. Texto con marcado simple de ReportLab: <b>negrita</b>, <i>cursiva</i>.
Solo caracteres de Windows-1252 (el generador lo valida).
"""

GUIA = {
    'key': 'manip',
    'course': 'Manipulación de Alimentos',
    'cover_title': 'Manipulación de Alimentos',
    'subtitle': 'Buenas Prácticas de Manufactura (BPM) para trabajar con alimentos en Colombia, '
                'según la Resolución 2674 de 2013.',
    'keywords': 'manipulación de alimentos, BPM, Resolución 2674 de 2013, guía de estudio',
    'chips': ['8 capítulos', 'Repaso con respuestas', 'Edición 2026'],
    'features': [
        ('Basada en la norma', 'Resolución 2674 de 2013 y buenas prácticas de higiene.'),
        ('Lista para usar', 'Pasos, tablas y listas de chequeo para tu día a día.'),
        ('Prepárate para el examen', '20 preguntas de repaso con sus respuestas.'),
    ],
    'cover_note': 'Esta guía es tuya y es gratis. Úsala para estudiar antes del examen, repasar los temas '
                  'del certificado y consultarla en tu trabajo cada vez que tengas una duda.',
    'how_to': 'Lee un capítulo a la vez. Fíjate en los recuadros de colores: <b>Recuerda</b> (azul) resume lo '
              'esencial, <b>Atención</b> (naranja) señala errores frecuentes y <b>Dato clave</b> (verde) destaca '
              'cifras que debes memorizar. Al final encontrarás un repaso de 20 preguntas con respuestas y un glosario.',

    'blocks': [
        # ─────────────────────────────────────────────────────────
        ('chapter', 'Atención y servicio al cliente',
         'En un establecimiento de alimentos la higiene también es parte del servicio: el cliente confía en que '
         'lo que come es seguro.'),
        ('p', 'El manipulador de alimentos es la cara visible del negocio. Tu presentación personal, tu forma de '
              'hablar y la manera en que manejas los alimentos frente al cliente transmiten confianza (o desconfianza) '
              'en pocos segundos.'),
        ('h2', 'Principios del buen servicio'),
        ('bullets', [
            '<b>Presentación impecable:</b> uniforme limpio, cabello cubierto, uñas cortas y sin joyas. El cliente lo '
            'nota antes de probar el producto.',
            '<b>Saludo y actitud:</b> saluda, mira a los ojos y usa un tono amable. Escucha el pedido completo antes de responder.',
            '<b>Información veraz:</b> si te preguntan por los ingredientes, no adivines. Consulta la receta o pregunta a tu jefe.',
            '<b>Rapidez con seguridad:</b> atender rápido nunca justifica saltarse el lavado de manos o servir un alimento dudoso.',
            '<b>Orden y limpieza visibles:</b> mostradores, vitrinas y área de servicio limpios generan confianza.',
        ]),
        ('h2', 'Alérgenos: una pregunta que puede salvar una vida'),
        ('p', 'Algunas personas tienen reacciones graves con cantidades muy pequeñas de ciertos alimentos. Los alérgenos '
              'más comunes son: <b>maní, frutos secos (nueces, almendras), leche, huevo, pescado, mariscos, trigo '
              '(gluten) y soya</b>.'),
        ('callout', 'warn', 'Si un cliente dice que es alérgico',
         'Avisa a la cocina, usa utensilios y superficies limpios y nunca respondas «no tiene» si no estás seguro. '
         'Una respuesta equivocada puede causar una reacción grave.'),
        ('h2', 'Manejo de quejas en 4 pasos'),
        ('steps', [
            ('Escucha sin interrumpir', 'Deja que el cliente explique. No te defiendas ni discutas.'),
            ('Ofrece una disculpa', 'Agradece que lo haya dicho: una queja es una oportunidad para mejorar.'),
            ('Soluciona o escala', 'Cambia el producto si aplica o informa de inmediato a tu jefe.'),
            ('Registra y aprende', 'Si la queja es por un posible problema de higiene o un objeto extraño en la comida, '
                                   'guarda el producto y repórtalo: puede evitar un problema mayor.'),
        ]),
        ('callout', 'info', 'Dinero y alimentos no se mezclan',
         'Evita manipular dinero y alimentos al mismo tiempo. Si debes hacerlo, lávate las manos antes de volver a '
         'tocar los alimentos o usa pinzas.'),

        # ─────────────────────────────────────────────────────────
        ('chapter', 'Legislación alimentaria en Colombia',
         'Conoce las normas que regulan tu trabajo y por qué la formación en manipulación de alimentos es obligatoria.'),
        ('h2', '¿Quién es manipulador de alimentos?'),
        ('p', 'Según la normatividad sanitaria colombiana, es manipulador de alimentos <b>toda persona que interviene '
              'directamente, aunque sea de forma ocasional, en actividades de fabricación, procesamiento, preparación, '
              'envase, almacenamiento, transporte y expendio de alimentos</b>.'),
        ('p', 'Esto incluye a cocineros, auxiliares de cocina, meseros, panaderos, vendedores de comidas, personal de '
              'bodegas de alimentos y conductores que transportan alimentos, entre otros.'),
        ('h2', 'Normas que debes conocer'),
        ('table', ['Norma', 'Qué establece'], [
            ['Ley 9 de 1979', 'Código Sanitario Nacional: base de las medidas sanitarias para proteger la salud de la '
                              'población, incluidos los alimentos.'],
            ['Decreto 3075 de 1997', 'Durante años fue la norma de referencia sobre Buenas Prácticas de Manufactura (BPM) en alimentos.'],
            ['Resolución 2674 de 2013', 'Norma del Ministerio de Salud y Protección Social que establece los requisitos '
                                        'sanitarios para quienes fabrican, procesan, preparan, envasan, almacenan, '
                                        'transportan, distribuyen y comercializan alimentos.'],
            ['Resolución 2184 de 2019', 'Código de colores unificado para separar los residuos en la fuente (blanco, negro y verde).'],
        ], [1, 2.6]),
        ('h2', 'Lo que la Resolución 2674 de 2013 exige al manipulador'),
        ('bullets', [
            '<b>Estado de salud:</b> haber pasado por un reconocimiento médico antes de desempeñar la función, y '
            'repetirlo cuando sea necesario por razones clínicas o epidemiológicas.',
            '<b>Educación y capacitación:</b> formación en educación sanitaria, principios básicos de Buenas Prácticas '
            'de Manufactura y prácticas higiénicas. La empresa debe tener un plan de capacitación continuo y permanente '
            'de <b>mínimo 10 horas al año</b>.',
            '<b>Prácticas higiénicas:</b> higiene personal, uniforme adecuado, lavado de manos y conductas seguras '
            'durante el trabajo (las verás en el capítulo 4).',
        ]),
        ('callout', 'key', 'Capacitación continua: mínimo 10 horas al año',
         'Como la capacitación debe ser continua, lo recomendable es actualizar tu certificado cada año y tenerlo '
         'disponible para las visitas de inspección.'),
        ('h2', '¿Quién vigila?'),
        ('p', 'Las <b>secretarías de salud</b> (departamentales, distritales y municipales) inspeccionan restaurantes, '
              'cafeterías, panaderías, tiendas y demás establecimientos donde se preparan o venden alimentos. El '
              '<b>INVIMA</b> vigila principalmente a las fábricas de alimentos y expide los registros, permisos y '
              'notificaciones sanitarias de los productos.'),
        ('p', 'Cuando encuentran incumplimientos, las autoridades pueden aplicar medidas sanitarias como el decomiso o '
              'la destrucción de productos, la suspensión de actividades o la clausura del establecimiento, además de '
              'sanciones económicas.'),
        ('h2', '¿Qué son las Buenas Prácticas de Manufactura (BPM)?'),
        ('p', 'Son los principios básicos y prácticas generales de higiene en la manipulación, preparación, elaboración, '
              'envasado, almacenamiento, transporte y distribución de alimentos. Su objetivo es garantizar que los '
              'productos se elaboren en condiciones sanitarias adecuadas y disminuir los riesgos para el consumidor.'),

        # ─────────────────────────────────────────────────────────
        ('chapter', 'Factores de contaminación de los alimentos',
         'Entiende cómo se contaminan los alimentos y qué los convierte en un riesgo para la salud.'),
        ('h2', 'Inocuidad: el objetivo de todo manipulador'),
        ('p', 'Un alimento <b>inocuo</b> es aquel que no causa daño al consumidor cuando se prepara y se consume de '
              'acuerdo con su uso previsto. Ojo: un alimento puede verse, oler y saber normal y aun así estar contaminado.'),
        ('h2', 'Los tres tipos de contaminación'),
        ('table', ['Tipo', 'Ejemplos', 'Cómo prevenirla'], [
            ['Biológica', 'Bacterias, virus, parásitos y hongos.',
             'Lavado de manos, cocción completa, control de temperaturas y evitar la contaminación cruzada.'],
            ['Química', 'Productos de limpieza, plaguicidas, exceso de aditivos.',
             'Guardar los químicos separados y rotulados, enjuagar bien y respetar las dosis.'],
            ['Física', 'Cabellos, vidrio, metal, plástico, piedras, joyas, astillas.',
             'Cabello cubierto, cero joyas, revisar las materias primas y reportar utensilios rotos.'],
        ], [0.8, 1.5, 2]),
        ('p', 'También existen los <b>alérgenos</b> (capítulo 1): no hacen daño a todas las personas, pero son un '
              'peligro grave para quienes son alérgicos.'),
        ('h2', 'Enfermedades Transmitidas por Alimentos (ETA)'),
        ('p', 'Las ETA se producen al consumir alimentos o agua contaminados. Los síntomas más comunes son diarrea, '
              'vómito, dolor abdominal, náuseas y fiebre. Pueden ser graves, incluso mortales, en <b>niños pequeños, '
              'mujeres embarazadas, adultos mayores y personas con defensas bajas</b>.'),
        ('table', ['Microorganismo', 'Alimentos asociados', 'Dato importante'], [
            ['Salmonella', 'Huevos, pollo y carnes crudos o mal cocidos.', 'Se elimina con una cocción completa.'],
            ['Escherichia coli (E. coli)', 'Carne molida mal cocida, agua contaminada, verduras mal lavadas.',
             'Algunas cepas causan enfermedad grave.'],
            ['Staphylococcus aureus', 'Alimentos que se manipulan con las manos: sándwiches, ensaladas, postres.',
             'Vive en la piel, la nariz y las heridas del manipulador.'],
            ['Listeria monocytogenes', 'Lácteos sin pasteurizar, quesos frescos, embutidos.',
             'Puede crecer incluso en refrigeración.'],
            ['Bacillus cereus', 'Arroz y pastas cocidos que se dejan a temperatura ambiente.',
             'Algunas de sus toxinas resisten el recalentamiento.'],
            ['Clostridium perfringens', 'Preparaciones en gran cantidad que se enfrían lentamente (guisos, sopas).',
             'Enfría rápido, en porciones pequeñas.'],
            ['Norovirus y hepatitis A', 'Alimentos listos para consumir, mariscos, agua.',
             'Se transmiten por manos mal lavadas.'],
        ], [1.25, 1.75, 1.5]),
        ('h2', '¿Qué necesitan las bacterias para multiplicarse?'),
        ('bullets', [
            '<b>Alimento:</b> sobre todo alimentos ricos en proteína y humedad.',
            '<b>Humedad:</b> los alimentos húmedos favorecen su crecimiento.',
            '<b>Temperatura:</b> crecen rápidamente entre 5 °C y 60 °C.',
            '<b>Tiempo:</b> en condiciones favorables una bacteria puede duplicarse aproximadamente cada 20 minutos.',
        ]),
        ('callout', 'warn', 'Zona de peligro: entre 5 °C y 60 °C',
         'En este rango las bacterias se multiplican rápidamente. Mantén los alimentos fríos a 5 °C o menos y los '
         'calientes por encima de 60 °C. No dejes alimentos cocinados más de 2 horas a temperatura ambiente.'),
        ('h2', 'Alimentos de alto riesgo'),
        ('p', 'Carnes, pollo, pescados y mariscos, huevos, leche y derivados, arroz y pastas cocidos, salsas y '
              'preparaciones con mayonesa o crema. Requieren un control estricto de temperatura y tiempo.'),
        ('h2', 'Contaminación cruzada'),
        ('p', 'Ocurre cuando los microorganismos pasan de un alimento contaminado (generalmente crudo) a uno que ya está '
              'listo para consumir.'),
        ('bullets', [
            '<b>Directa:</b> un alimento crudo toca uno cocido. Por ejemplo, el jugo del pollo crudo gotea sobre una ensalada.',
            '<b>Indirecta:</b> a través de manos, tablas, cuchillos, trapos o superficies que tocaron el alimento crudo '
            'y luego el cocido sin lavarse.',
        ]),
        ('h3', 'Cómo evitarla'),
        ('bullets', [
            'Usa tablas y utensilios diferentes para crudos y cocidos.',
            'Lava y desinfecta superficies y utensilios entre una tarea y otra.',
            'Lávate las manos después de tocar alimentos crudos.',
            'En la nevera guarda arriba los alimentos cocidos y listos para consumir, y abajo las carnes crudas, '
            'siempre en recipientes tapados.',
        ]),
        ('h3', 'Ejemplo de código de colores para tablas de picar'),
        ('table', ['Color', 'Uso'], [
            ['Rojo', 'Carnes rojas crudas'],
            ['Amarillo', 'Aves crudas'],
            ['Azul', 'Pescados y mariscos crudos'],
            ['Verde', 'Frutas y verduras'],
            ['Blanco', 'Lácteos y panadería'],
            ['Café', 'Alimentos cocidos'],
        ], [1, 3]),
        ('small', 'Es una convención común en cocinas, no una exigencia legal. Sigue el código que use tu establecimiento.'),

        # ─────────────────────────────────────────────────────────
        ('chapter', 'Normas y hábitos del manipulador',
         'Tus manos, tu ropa y tus hábitos son la primera barrera contra la contaminación.'),
        ('h2', 'Estado de salud'),
        ('p', 'Si presentas alguno de estos síntomas, <b>informa a tu jefe antes de empezar el turno</b> y no manipules '
              'alimentos hasta que te lo autoricen:'),
        ('bullets', [
            'Diarrea o vómito.',
            'Fiebre.',
            'Coloración amarilla de la piel o de los ojos.',
            'Dolor de garganta con fiebre.',
            'Heridas infectadas, quemaduras o lesiones en la piel.',
            'Secreciones por los oídos, los ojos o la nariz.',
        ]),
        ('p', 'Las heridas pequeñas se cubren con un apósito impermeable de color visible y, encima, se usa guante.'),
        ('h2', 'Lavado de manos: cuándo'),
        ('bullets', [
            'Al iniciar la jornada y cada vez que vuelvas al área de trabajo.',
            'Después de ir al baño.',
            'Después de tocar alimentos crudos (carnes, pollo, huevos, verduras sin lavar).',
            'Después de tocar basura, dinero, el celular, la cara, el cabello o la nariz.',
            'Después de toser, estornudar o sonarte.',
            'Después de limpiar o de usar productos químicos.',
            'Al cambiar de tarea y antes de ponerte guantes.',
        ]),
        ('h2', 'Lavado de manos: cómo'),
        ('steps', [
            ('Moja las manos y los antebrazos', 'Usa agua potable.'),
            ('Aplica jabón', 'Suficiente para cubrir toda la superficie de las manos; idealmente jabón desinfectante.'),
            ('Frota durante al menos 20 segundos', 'Palmas, dorso, entre los dedos, pulgares, yemas, uñas y muñecas.'),
            ('Enjuaga', 'Con abundante agua, hasta retirar todo el jabón.'),
            ('Seca', 'Con toalla desechable o secador de aire. Nunca con el delantal o el uniforme.'),
            ('Cierra la llave con la toalla', 'Y luego deséchala.'),
        ]),
        ('callout', 'key', 'El lavado completo toma entre 40 y 60 segundos',
         'Los guantes no reemplazan el lavado de manos: lávate antes de ponértelos y cámbialos cuando se rompan, '
         'se ensucien o cambies de tarea.'),
        ('h2', 'Presentación personal'),
        ('table', ['Elemento', 'Cómo debe estar'], [
            ['Uniforme', 'De color claro y limpio, con cierres o broches en lugar de botones y sin bolsillos por encima '
                         'de la cintura. Solo se usa en el lugar de trabajo.'],
            ['Cabello', 'Recogido y totalmente cubierto con gorro, cofia o malla.'],
            ['Barba y bigote', 'Cubiertos con protector.'],
            ['Uñas', 'Cortas, limpias y sin esmalte.'],
            ['Joyas y accesorios', 'No se permiten reloj, anillos, aretes, pulseras ni piercings.'],
            ['Maquillaje', 'No está permitido en el área de trabajo.'],
            ['Calzado', 'Cerrado, resistente, impermeable y de tacón bajo.'],
            ['Tapabocas', 'Cuando sea necesario, cubriendo nariz y boca.'],
            ['Guantes', 'Limpios y sin roturas; se cambian con frecuencia.'],
        ], [1, 3]),
        ('h2', 'Conductas prohibidas en el área de alimentos'),
        ('bullets', [
            'Comer, beber o masticar chicle.',
            'Fumar o escupir.',
            'Toser o estornudar sobre los alimentos.',
            'Probar la comida con los dedos o con el mismo utensilio con el que se revuelve.',
            'Usar el celular mientras manipulas alimentos.',
            'Secarte el sudor o las manos con el delantal o el uniforme.',
        ]),
        ('checklist', 'Lista de chequeo antes de iniciar tu turno', [
            'Me siento bien y no tengo síntomas de enfermedad.',
            'Uniforme limpio y completo.',
            'Cabello recogido y totalmente cubierto.',
            'Uñas cortas, limpias y sin esmalte.',
            'Sin joyas, reloj ni maquillaje.',
            'Heridas cubiertas con apósito impermeable.',
            'Manos lavadas correctamente.',
            'Celular y objetos personales guardados fuera del área.',
        ]),

        # ─────────────────────────────────────────────────────────
        ('chapter', 'Limpieza de instalaciones, equipos y utensilios',
         'Limpiar y desinfectar no es lo mismo: aprende a hacer ambas cosas bien y en el orden correcto.'),
        ('h2', 'Limpiar no es lo mismo que desinfectar'),
        ('table', ['', 'Limpieza', 'Desinfección'], [
            ['Qué hace', 'Retira la suciedad visible, la grasa y los restos de alimentos.',
             'Reduce los microorganismos a niveles seguros.'],
            ['Con qué', 'Agua, detergente y acción mecánica (cepillo, esponja).',
             'Un desinfectante (por ejemplo, hipoclorito de sodio) o calor.'],
            ['Cuándo', 'Siempre primero.', 'Siempre después de limpiar.'],
        ], [0.8, 1.6, 1.6]),
        ('callout', 'warn', 'Primero se limpia, después se desinfecta',
         'El desinfectante no funciona bien sobre una superficie sucia: la grasa y los residuos lo inactivan.'),
        ('h2', 'Procedimiento en 6 pasos'),
        ('steps', [
            ('Retira los residuos', 'Elimina los restos de comida con una espátula o papel y deséchalos.'),
            ('Prelava', 'Enjuaga con agua para retirar la suciedad suelta.'),
            ('Lava', 'Aplica detergente y frota con cepillo o esponja.'),
            ('Enjuaga', 'Retira todo el detergente con agua potable.'),
            ('Desinfecta', 'Aplica el desinfectante con la concentración y el tiempo de contacto indicados.'),
            ('Seca', 'Deja secar al aire o usa toallas desechables. Si el producto lo indica, enjuaga antes de secar.'),
        ]),
        ('h2', 'Frecuencias sugeridas'),
        ('table', ['Qué', 'Cuándo'], [
            ['Mesas y superficies de trabajo', 'Antes y después de usarlas y al cambiar de tarea, sobre todo de crudo a cocido.'],
            ['Tablas, cuchillos y utensilios', 'Después de cada uso.'],
            ['Equipos (licuadoras, cortadoras, molinos)', 'Al terminar de usarlos, desarmando las piezas que se puedan.'],
            ['Pisos', 'Todos los días y cada vez que se ensucien.'],
            ['Neveras y congeladores', 'Limpieza general periódica según el plan de saneamiento (por ejemplo, semanal).'],
            ['Canecas de basura', 'Todos los días.'],
            ['Paredes, techos y campanas extractoras', 'Según el plan de saneamiento del establecimiento.'],
        ], [1.4, 2.4]),
        ('small', 'Las frecuencias exactas las define el plan de saneamiento de cada establecimiento.'),
        ('h2', 'Trapos, esponjas y paños'),
        ('p', 'Son una de las principales fuentes de contaminación cruzada porque acumulan humedad y residuos. Prefiere '
              'toallas desechables. Si usas paños, ten paños distintos para cada área, lávalos y desinféctalos con '
              'frecuencia y cámbialos cuando estén deteriorados.'),
        ('h2', 'Lavado y desinfección de frutas y verduras'),
        ('steps', [
            ('Selecciona', 'Retira hojas dañadas y partes en mal estado.'),
            ('Lava', 'Con agua potable, frotando la superficie.'),
            ('Desinfecta', 'Con un producto apto para alimentos, respetando la dosis y el tiempo de contacto de la etiqueta.'),
            ('Enjuaga y guarda', 'Enjuaga si la etiqueta lo indica y guarda en recipientes limpios y tapados.'),
        ]),
        ('h2', 'El plan de saneamiento'),
        ('p', 'La Resolución 2674 de 2013 exige que los establecimientos tengan un plan de saneamiento con objetivos, '
              'procedimientos, responsables y registros. Como mínimo incluye cuatro programas:'),
        ('bullets', [
            'Limpieza y desinfección.',
            'Manejo de residuos sólidos.',
            'Control de plagas.',
            'Abastecimiento de agua potable.',
        ]),

        # ─────────────────────────────────────────────────────────
        ('chapter', 'Preparación de productos químicos para desinfección',
         'Usar bien los químicos protege los alimentos y tu salud. Una mala dilución no desinfecta o puede contaminar.'),
        ('h2', 'Tipos de productos'),
        ('table', ['Producto', 'Para qué sirve', 'Ejemplos'], [
            ['Detergentes', 'Retirar la grasa y la suciedad.', 'Detergente líquido o en polvo, desengrasantes.'],
            ['Desinfectantes', 'Reducir microorganismos en superficies, equipos y utensilios.',
             'Hipoclorito de sodio, amonios cuaternarios, ácido peracético.'],
            ['Desinfectantes para alimentos', 'Desinfectar frutas y verduras.',
             'Productos cuya etiqueta indique que son aptos para alimentos.'],
            ['Alcohol al 70 %', 'Desinfectar superficies pequeñas y utensilios ya limpios y secos.', 'Alcohol antiséptico.'],
        ], [1.1, 1.6, 1.6]),
        ('h2', 'Concentración: ¿qué son las ppm?'),
        ('p', 'La concentración de un desinfectante se expresa en <b>partes por millón (ppm)</b>: 1 ppm equivale a 1 mg '
              'de producto activo por litro de solución. El hipoclorito de uso doméstico suele venir alrededor del 5 % '
              '(aproximadamente 50.000 ppm); por eso siempre se diluye en agua antes de usarlo.'),
        ('h2', 'Fórmula de dilución'),
        ('formula', 'C1 × V1 = C2 × V2', [
            '<b>C1:</b> concentración del producto comercial (por ejemplo, 50.000 ppm).',
            '<b>V1:</b> cantidad de producto comercial que debes medir (lo que quieres averiguar).',
            '<b>C2:</b> concentración que necesitas en la solución (por ejemplo, 200 ppm).',
            '<b>V2:</b> volumen de solución que vas a preparar.',
            'Despejando: <b>V1 = (C2 × V2) ÷ C1</b>',
        ]),
        ('h3', 'Ejemplo 1'),
        ('p', 'Necesitas 1 litro (1.000 ml) de solución a 200 ppm y tienes hipoclorito al 5 % (50.000 ppm):<br/>'
              'V1 = (200 × 1.000) ÷ 50.000 = <b>4 ml</b>. Mides 4 ml de hipoclorito y completas con agua hasta 1 litro.'),
        ('h3', 'Ejemplo 2'),
        ('p', 'Necesitas 10 litros (10.000 ml) a 100 ppm con el mismo hipoclorito al 5 %:<br/>'
              'V1 = (100 × 10.000) ÷ 50.000 = <b>20 ml</b>. Mides 20 ml y completas con agua hasta 10 litros.'),
        ('callout', 'key', 'Usa la concentración indicada, ni más ni menos',
         'Sigue la ficha técnica del producto y el plan de saneamiento de tu establecimiento. Poner más cantidad no '
         'desinfecta mejor: puede dejar residuos químicos en los alimentos y dañar los equipos.'),
        ('h2', 'Reglas de seguridad'),
        ('bullets', [
            'Lee la etiqueta y la hoja de seguridad del producto antes de usarlo.',
            'Usa guantes y, si el producto lo indica, gafas y tapabocas.',
            'Prepara las soluciones en un lugar ventilado y con agua fría.',
            'Mide con un recipiente medidor; no calcules «a ojo».',
            '<b>Nunca mezcles</b> cloro con amoníaco, vinagre, ácidos u otros limpiadores: se liberan gases tóxicos.',
            'Nunca reenvases químicos en botellas de bebidas ni en recipientes de alimentos.',
            'Rotula cada recipiente con el nombre del producto, la concentración y la fecha de preparación.',
            'Prepara la solución de hipoclorito para el día: pierde efectividad con el tiempo, la luz y el calor.',
            'Guarda los químicos en un lugar exclusivo, rotulado y separado de los alimentos.',
        ]),
        ('callout', 'warn', 'En caso de accidente',
         'Si el producto cae en los ojos, lávalos con abundante agua durante al menos 15 minutos. Si hay contacto con '
         'la piel, enjuaga con agua. Si alguien lo inhala o lo ingiere, sigue las instrucciones de la hoja de seguridad '
         'y busca atención médica de inmediato.'),
        ('h2', 'Pictogramas de peligro'),
        ('p', 'Las etiquetas de los químicos usan los pictogramas del Sistema Globalmente Armonizado (SGA): rombos con '
              'borde rojo que indican si el producto es corrosivo, inflamable, tóxico, irritante o peligroso para el '
              'medio ambiente. Identifícalos antes de usar cualquier producto.'),

        # ─────────────────────────────────────────────────────────
        ('chapter', 'Manejo de insumos y residuos',
         'Desde que llega la materia prima hasta que se sirve el plato... y hasta que sale la basura.'),
        ('h2', 'Recepción de materias primas'),
        ('bullets', [
            'Revisa el vehículo y las condiciones de transporte: limpio y refrigerado cuando aplique.',
            'Verifica que los empaques estén completos, sin golpes, abombamientos, roturas ni humedad.',
            'Revisa la fecha de vencimiento, el lote y el registro sanitario de los productos empacados.',
            'Mide la temperatura de los refrigerados y congelados.',
            'Evalúa el olor, el color y la textura (características organolépticas).',
            'Separa y reporta lo que no cumple; no lo recibas como si estuviera bien.',
        ]),
        ('h2', 'Temperaturas de referencia'),
        ('table', ['Situación', 'Temperatura'], [
            ['Refrigeración', '5 °C o menos.'],
            ['Congelación', '-18 °C o menos.'],
            ['Cocción', 'Al menos 70 °C en el centro del alimento.'],
            ['Mantenimiento en caliente', 'Por encima de 60 °C.'],
            ['Recalentamiento', 'Hasta que esté bien caliente (al menos 70 °C), y una sola vez.'],
            ['Alimentos cocinados a temperatura ambiente', 'Máximo 2 horas.'],
        ], [1.6, 2.4]),
        ('h2', 'Almacenamiento'),
        ('bullets', [
            'Aplica <b>PEPS</b>: lo primero que entra es lo primero que sale. En perecederos, lo primero que vence es '
            'lo primero que sale.',
            'Almacena sobre estibas o estantes, separado del piso y de las paredes, para facilitar la limpieza y la inspección.',
            'Mantén los recipientes tapados y rotulados con el nombre, la fecha de preparación o apertura y la fecha de vencimiento.',
            'Guarda los productos de limpieza en un área exclusiva, lejos de los alimentos.',
            'No sobrecargues neveras ni congeladores: el frío necesita circular.',
            'Revisa y registra las temperaturas de los equipos de frío.',
        ]),
        ('h2', 'Descongelación segura'),
        ('bullets', [
            'En la nevera: es la forma más segura; planifica con tiempo.',
            'En el microondas, solo si vas a cocinar el alimento de inmediato.',
            'Bajo un chorro de agua fría, con el alimento dentro de su empaque cerrado.',
            '<b>Nunca</b> a temperatura ambiente sobre el mesón.',
            'No vuelvas a congelar un alimento crudo que ya se descongeló, a menos que primero lo cocines.',
        ]),
        ('h2', 'Enfriamiento de preparaciones'),
        ('p', 'Divide las preparaciones grandes en recipientes pequeños y poco profundos y llévalas a refrigeración lo '
              'antes posible, dentro de las 2 horas siguientes a la cocción.'),
        ('h2', 'Manejo de residuos'),
        ('p', 'Los residuos atraen plagas y son una fuente de contaminación. Deben retirarse con frecuencia del área de '
              'preparación y almacenarse lejos de los alimentos.'),
        ('bullets', [
            'Usa canecas con tapa (ideal de pedal) y bolsa.',
            'Retira la basura del área cuantas veces sea necesario y siempre al final de la jornada.',
            'Lava y desinfecta las canecas todos los días.',
            'Lávate las manos después de manipular residuos.',
            'El aceite de cocina usado no se bota por el desagüe: entrégalo a un gestor autorizado (Resolución 316 de 2018).',
        ]),
        ('h2', 'Control de plagas'),
        ('p', 'Cucarachas, moscas, roedores y hormigas transportan microorganismos. Señales de alerta: excrementos, '
              'huellas, empaques roídos, olores extraños o insectos vivos o muertos.'),
        ('bullets', [
            'No dejes restos de comida ni agua estancada.',
            'Mantén las puertas cerradas y mallas en ventanas y sifones.',
            'Sella grietas y huecos.',
            'Revisa la mercancía al recibirla.',
            'La aplicación de químicos la hace una empresa autorizada, nunca con alimentos expuestos.',
            'Reporta de inmediato cualquier señal de plagas.',
        ]),

        # ─────────────────────────────────────────────────────────
        ('chapter', 'Normas de bioseguridad y segregación en la fuente',
         'Medidas que protegen tu salud, la de tus compañeros y la de los clientes.'),
        ('h2', '¿Qué es la bioseguridad?'),
        ('p', 'Es el conjunto de medidas preventivas que buscan reducir el riesgo de transmisión de microorganismos en el '
              'lugar de trabajo. En un establecimiento de alimentos protege al mismo tiempo al trabajador y al consumidor.'),
        ('h2', 'Medidas básicas'),
        ('bullets', [
            'Higiene de manos frecuente (capítulo 4).',
            'Etiqueta respiratoria: al toser o estornudar, cúbrete con el codo o con un pañuelo desechable, lejos de los '
            'alimentos, y luego lávate las manos.',
            'Uso correcto de los elementos de protección personal (EPP): tapabocas, guantes, gorro y delantal según la tarea.',
            'Limpieza y desinfección frecuente de las superficies de alto contacto: manijas, interruptores, datáfonos, '
            'mostradores y menús.',
            'No compartir objetos personales como vasos, cubiertos o toallas.',
            'Ventilar los espacios cuando sea posible.',
            'Si estás enfermo, repórtalo y no trabajes con alimentos.',
        ]),
        ('h2', 'Uso correcto del tapabocas y los guantes'),
        ('bullets', [
            'El tapabocas cubre nariz y boca; no se baja al mentón ni se toca por fuera.',
            'Cambia el tapabocas cuando esté húmedo o sucio.',
            'Cambia los guantes al cambiar de tarea, al tocar algo contaminado y cuando se rompan.',
            'Retira los guantes sin tocar la parte externa con la piel y lávate las manos.',
        ]),
        ('h2', 'Segregación en la fuente'),
        ('p', 'Separar en la fuente significa clasificar los residuos <b>en el mismo lugar donde se generan</b>, en el '
              'recipiente correcto. Así se facilita el reciclaje y se evita que los residuos contaminados se mezclen con '
              'los aprovechables. Colombia usa un código de colores unificado (Resolución 2184 de 2019):'),
        ('colors', [
            ('#ffffff', '#0f172a', 'BLANCA', 'Aprovechables', 'Plástico, vidrio, metales, papel y cartón limpios y secos.'),
            ('#111827', '#ffffff', 'NEGRA', 'No aprovechables', 'Servilletas y papeles sucios, papel higiénico, empaques '
                                                                 'contaminados con comida, papeles metalizados.'),
            ('#16a34a', '#ffffff', 'VERDE', 'Orgánicos aprovechables', 'Restos de comida, cáscaras, residuos de frutas y verduras.'),
        ]),
        ('callout', 'info', 'Antes de usar la caneca blanca',
         'Los envases deben estar vacíos, limpios y secos. Un envase con restos de comida contamina todo el material reciclable.'),

        # ─────────────────────────────────────────────────────────
        ('section', 'Repaso: pon a prueba lo que aprendiste', 'repaso',
         'Responde sin mirar y luego compara con las respuestas al final.'),
        ('quiz', [
            ('¿Cuál norma establece los requisitos sanitarios para quienes manipulan alimentos en Colombia?',
             ['Ley 100 de 1993', 'Resolución 2674 de 2013', 'Código Nacional de Tránsito'], 1),
            ('¿Cuántas horas al año debe tener como mínimo el plan de capacitación del manipulador?',
             ['2 horas', '10 horas', '40 horas'], 1),
            ('Un alimento inocuo es aquel que:', ['Tiene buen sabor', 'No le causa daño al consumidor', 'Viene empacado'], 1),
            ('Un cabello dentro de una sopa es una contaminación:', ['Física', 'Química', 'Biológica'], 0),
            ('¿Cuál es la zona de temperatura de peligro?', ['Entre 5 °C y 60 °C', 'Por debajo de -18 °C', 'Por encima de 70 °C'], 0),
            ('¿Cuánto tiempo máximo puede estar un alimento cocinado a temperatura ambiente?',
             ['2 horas', '8 horas', 'Todo el día'], 0),
            ('En la nevera, las carnes crudas se guardan:',
             ['En la parte de arriba', 'En la parte de abajo y tapadas', 'Junto a los postres'], 1),
            ('Durante el lavado de manos debes frotar con jabón al menos:', ['5 segundos', '20 segundos', '5 minutos'], 1),
            ('Los guantes:', ['Reemplazan el lavado de manos', 'Se cambian al cambiar de tarea o si se rompen',
                              'Se usan todo el día sin cambiarlos'], 1),
            ('¿Cómo deben estar las uñas del manipulador?',
             ['Largas pero limpias', 'Cortas, limpias y sin esmalte', 'Con esmalte transparente'], 1),
            ('Si tienes diarrea o fiebre, debes:',
             ['Trabajar con tapabocas', 'Informar a tu jefe y no manipular alimentos', 'Usar doble guante'], 1),
            ('¿Qué se hace primero?', ['Desinfectar', 'Limpiar', 'Da igual el orden'], 1),
            ('Para preparar 1 litro a 200 ppm con hipoclorito al 5 % (50.000 ppm), ¿cuánto hipoclorito necesitas?',
             ['4 ml', '40 ml', '200 ml'], 0),
            ('Nunca se debe mezclar el cloro con:', ['Agua fría', 'Amoníaco o vinagre', 'Agua potable'], 1),
            ('PEPS significa:', ['Primero en entrar, primero en salir', 'Preparar, empacar, pesar y servir',
                                 'Producto en peligro de salir'], 0),
            ('¿Cuál es la forma más segura de descongelar?', ['Sobre el mesón', 'En la nevera', 'Al sol'], 1),
            ('¿A qué temperatura mínima debe llegar el centro de un alimento al cocinarlo?', ['30 °C', '50 °C', '70 °C'], 2),
            ('Los restos de comida van en la caneca:', ['Blanca', 'Negra', 'Verde'], 2),
            ('Una servilleta sucia va en la caneca:', ['Blanca', 'Negra', 'Verde'], 1),
            ('La contaminación cruzada ocurre cuando:',
             ['Se cocina bien un alimento', 'Los microorganismos pasan de un alimento crudo a uno listo para consumir',
              'Se congela la carne'], 1),
        ]),

        ('section', 'Glosario', 'glosario'),
        ('glossary', [
            ('Alimento de alto riesgo', 'alimento que, por su composición, favorece el crecimiento de microorganismos '
                                        '(carnes, lácteos, huevos, arroz cocido, salsas).'),
            ('BPM', 'Buenas Prácticas de Manufactura: principios de higiene para producir alimentos seguros.'),
            ('Contaminación cruzada', 'paso de microorganismos de un alimento o superficie contaminados a un alimento listo para consumir.'),
            ('Desinfección', 'reducción de los microorganismos a niveles seguros mediante químicos o calor.'),
            ('ETA', 'Enfermedad Transmitida por Alimentos.'),
            ('Inocuidad', 'garantía de que un alimento no causará daño al consumidor.'),
            ('Limpieza', 'eliminación de la suciedad visible, la grasa y los restos de alimentos.'),
            ('Manipulador de alimentos', 'toda persona que interviene directamente, aunque sea de forma ocasional, en la '
                                         'fabricación, preparación, almacenamiento, transporte o expendio de alimentos.'),
            ('PEPS', 'primero en entrar, primero en salir.'),
            ('Plan de saneamiento', 'conjunto de programas escritos de limpieza y desinfección, residuos, control de plagas '
                                    'y agua potable de un establecimiento.'),
            ('ppm', 'partes por millón: unidad para expresar la concentración de un desinfectante.'),
            ('Segregación en la fuente', 'separación de los residuos en el mismo lugar donde se generan.'),
            ('Zona de peligro', 'rango de temperatura entre 5 °C y 60 °C en el que las bacterias se multiplican rápidamente.'),
        ]),
    ],

    'cta_title': 'Siguiente paso: tu certificado',
    'cta_text': [
        'Ya tienes las bases. Presenta el examen gratis en CertiTec y, al aprobarlo, recibe tu certificado de '
        'Manipulación de Alimentos.',
    ],
    'cta_bullets': [
        'Certificado en PDF a tu nombre y número de documento.',
        'Emitido y firmado por Alianza Capacitarte.',
        'Verificable en línea con tu número de documento.',
        'Soporte personalizado por WhatsApp.',
    ],
}
