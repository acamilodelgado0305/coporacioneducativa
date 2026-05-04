export interface Pregunta {
  q: string;
  options: string[];
  a: number;
}

export interface Beneficio {
  icono: string;
  titulo: string;
  desc: string;
  bg: string;
  color: string;
}

export interface Curso {
  slug: string;
  titulo: string;
  tituloResaltado: string;
  tagline: string;
  taglineEmoji: string;
  descripcionHero: string;
  precio: number;
  precioAnterior?: number;
  accentHex: string;        // color temático del curso
  badgeTexto?: string;
  badgeClase?: string;
  linkPago: string;
  nombreProducto: string;
  icono: string;            // Font Awesome class
  iconoSeccion: string;
  beneficios: Beneficio[];
  preguntas: Pregunta[];
  conRegistro?: boolean;
  webhookUrl?: string;
  negocioId?: number;
  usuarioId?: number;
  pixelEnabled?: boolean;
}

export const cursos: Curso[] = [
  {
    slug: 'manipulacion-de-alimentos',
    titulo: 'Manipulación de',
    tituloResaltado: 'Alimentos',
    tagline: 'Requisito Legal Obligatorio',
    taglineEmoji: '🍽️',
    descripcionHero: 'Cumple con la Resolución 2674/2013. Certificado + Carnet válido para restaurantes, tiendas y manipuladores.',
    precio: 22000,
    accentHex: '#15803d',
    badgeTexto: 'OBLIGATORIO',
    badgeClase: 'bg-red-600',
    linkPago: 'https://checkout.nequi.wompi.co/l/bSxc9E',
    nombreProducto: 'Certificado Manipulación de Alimentos',
    icono: 'fa-utensils',
    iconoSeccion: 'fa-utensils',
    beneficios: [
      { icono: 'fa-file-contract', titulo: 'Cumplimiento Legal', desc: 'Obligatorio según Resolución 2674/2013 del Ministerio de Salud.', bg: 'bg-green-100', color: 'text-green-600' },
      { icono: 'fa-shield-alt', titulo: 'Prevención de ETAs', desc: 'Aprende a evitar enfermedades de transmisión alimentaria.', bg: 'bg-blue-100', color: 'text-blue-600' },
      { icono: 'fa-laptop', titulo: 'Sin Horarios', desc: 'Estudia y presenta el examen desde tu celular en 15 minutos.', bg: 'bg-purple-100', color: 'text-purple-600' },
    ],
    conRegistro: true,
    webhookUrl: 'https://n8n.certitecol.com/webhook/6a03322d-f85e-46df-a0f4-fb27010a6b0c',
    negocioId: 3,
    usuarioId: 25,
    pixelEnabled: true,
    preguntas: [
      { q: '¿Cuál es la norma principal que regula la manipulación de alimentos en Colombia?', options: ['Resolución 2674 de 2013', 'Código de Policía', 'Ley 100'], a: 0 },
      { q: 'La contaminación cruzada ocurre cuando:', options: ['Se lavan bien los alimentos', 'Se mezclan alimentos crudos con cocidos', 'Se congela la carne'], a: 1 },
      { q: '¿Cuánto tiempo mínimo debe durar el lavado de manos?', options: ['5 segundos', '20 a 30 segundos con jabón', 'Solo enjuagar con agua'], a: 1 },
      { q: '¿Cuál es la zona de temperatura de peligro para los alimentos?', options: ['Entre 5°C y 60°C', 'Menos de 0°C', 'Más de 100°C'], a: 0 },
      { q: 'Si tienes gripe o heridas en las manos, ¿qué debes hacer?', options: ['Usar tapabocas y seguir trabajando', 'Informar al jefe y no manipular alimentos', 'Ponerse doble guante'], a: 1 },
      { q: 'El agua utilizada para preparar alimentos debe ser:', options: ['De río', 'Potable', 'Lluvia'], a: 1 },
      { q: '¿Cómo se deben almacenar los productos químicos de aseo?', options: ['Junto a la comida para tenerlos cerca', 'En un lugar separado y rotulado', 'En la nevera'], a: 1 },
      { q: 'El carnet de manipulación de alimentos tiene validez ante:', options: ['Solo el restaurante donde trabajo', 'Secretaría de Salud (Nacional)', 'La policía de tránsito'], a: 1 },
    ],
  },

  {
    slug: 'bioseguridad',
    titulo: 'Bioseguridad',
    tituloResaltado: 'General',
    tagline: 'Requisito para el Sector Salud y Estética',
    taglineEmoji: '🛡️',
    descripcionHero: 'Protocolos esenciales para establecimientos de belleza, salud y estética. Certificado con validez nacional.',
    precio: 50000,
    accentHex: '#7c3aed',
    badgeTexto: 'SALUD',
    badgeClase: 'bg-purple-600',
    linkPago: 'https://checkout.nequi.wompi.co/l/rxZMK8',
    nombreProducto: 'Certificado Bioseguridad General',
    icono: 'fa-shield-virus',
    iconoSeccion: 'fa-shield-virus',
    beneficios: [
      { icono: 'fa-file-contract', titulo: 'Exigido en el Sector Salud', desc: 'Requisito para trabajar en clínicas, estéticas y centros médicos.', bg: 'bg-purple-100', color: 'text-purple-600' },
      { icono: 'fa-user-shield', titulo: 'Protege tu Entorno', desc: 'Aprende el uso correcto de EPP y manejo de residuos biológicos.', bg: 'bg-blue-100', color: 'text-blue-600' },
      { icono: 'fa-laptop', titulo: 'Sin Horarios', desc: 'Certifícate desde tu celular en 20 minutos.', bg: 'bg-indigo-100', color: 'text-indigo-600' },
    ],
    pixelEnabled: true,
    preguntas: [
      { q: 'El principio que establece tomar precauciones con TODAS las personas por igual se llama:', options: ['Barrera de Protección', 'Universalidad', 'Aislamiento Selectivo'], a: 1 },
      { q: '¿Cuál es el objetivo principal de la Esterilización?', options: ['Limpiar la suciedad visible', 'Eliminar la mayoría de bacterias', 'Destruir TODA forma de vida microbiana'], a: 2 },
      { q: 'Las agujas y elementos cortopunzantes se desechan OBLIGATORIAMENTE en:', options: ['Bolsa Roja', 'Guardián de Seguridad Rígido', 'Bolsa Negra Doble'], a: 1 },
      { q: '¿Qué EPP protege principalmente las vías respiratorias contra aerosoles?', options: ['Guantes de látex', 'Gorro desechable', 'Mascarilla / Tapabocas'], a: 2 },
      { q: 'Antes de cualquier proceso de desinfección, el PRIMER paso indispensable es:', options: ['Limpieza profunda (Agua y Jabón)', 'Secado con aire caliente', 'Aplicación de alcohol al 70%'], a: 0 },
      { q: 'Los residuos comunes no peligrosos (papel, cartón limpio) van en bolsa color:', options: ['Roja', 'Negra o Verde', 'Solo en Guardián'], a: 1 },
      { q: '¿La Desinfección de alto nivel garantiza la eliminación de esporas bacterianas?', options: ['Sí, siempre las elimina', 'No necesariamente elimina esporas', 'Solo si se hierve 1 hora'], a: 1 },
      { q: '¿En qué color de bolsa van los residuos con riesgo biológico (gasas con sangre)?', options: ['Verde', 'Gris', 'Roja'], a: 2 },
    ],
  },

  {
    slug: 'limpieza-hospitalaria',
    titulo: 'Limpieza y Desinfección',
    tituloResaltado: 'Hospitalaria',
    tagline: 'Requisito para Contratación',
    taglineEmoji: '🏥',
    descripcionHero: 'Certifícate en protocolos de aseo para Clínicas, Hospitales y Centros de Salud. 100% Válido y Online.',
    precio: 50000,
    accentHex: '#1d4ed8',
    badgeTexto: 'SALUD',
    badgeClase: 'bg-blue-600',
    linkPago: 'https://checkout.nequi.wompi.co/l/rxZMK8',
    nombreProducto: 'Curso Aseo Hospitalario',
    icono: 'fa-pump-medical',
    iconoSeccion: 'fa-pump-medical',
    beneficios: [
      { icono: 'fa-file-contract', titulo: 'Mejora tu Hoja de Vida', desc: 'Indispensable para entrar a trabajar en el sector salud (Clínicas/IPS).', bg: 'bg-blue-100', color: 'text-blue-600' },
      { icono: 'fa-microscope', titulo: 'Aprende Protocolos Reales', desc: 'Manejo de áreas críticas, código de colores y residuos biológicos.', bg: 'bg-green-100', color: 'text-green-600' },
      { icono: 'fa-laptop', titulo: 'Sin Horarios', desc: 'Estudia y presenta el examen desde tu celular en 20 minutos.', bg: 'bg-purple-100', color: 'text-purple-600' },
    ],
    preguntas: [
      { q: 'La diferencia principal entre Limpiar y Desinfectar es:', options: ['Es lo mismo', 'Limpiar remueve suciedad visible, Desinfectar mata microorganismos', 'Desinfectar es usar solo agua'], a: 1 },
      { q: '¿Cuál es el desinfectante más usado en hospitales para superficies?', options: ['Jabón en polvo', 'Hipoclorito de Sodio (Cloro)', 'Alcohol al 10%'], a: 1 },
      { q: "La 'Limpieza Terminal' es aquella que se realiza:", options: ['Todos los días rápidamente', 'Al finalizar el alta del paciente (egreso)', 'Solo en los pasillos'], a: 1 },
      { q: 'Según la técnica de arrastre, se debe limpiar:', options: ['De lo más sucio a lo más limpio', 'De lo más limpio a lo más sucio', 'En círculos desordenados'], a: 1 },
      { q: "Las áreas 'Críticas' en un hospital son:", options: ['Oficinas administrativas', 'Quirófanos, Urgencias y UCI', 'Sala de espera general'], a: 1 },
      { q: '¿En qué color de bolsa van los residuos con riesgo biológico (gasas con sangre)?', options: ['Bolsa Gris', 'Bolsa Verde', 'Bolsa Roja'], a: 2 },
      { q: 'Antes de iniciar labores de aseo, es indispensable:', options: ['Lavarse las manos y ponerse los EPP', 'Comer algo rápido', 'Mezclar todos los químicos'], a: 0 },
      { q: "La limpieza 'Rutinaria' es aquella que se hace:", options: ['Una vez al mes', 'Diariamente mientras el paciente está en la habitación', 'Solo cuando hay auditoría'], a: 1 },
    ],
  },

  {
    slug: 'atencion-al-cliente',
    titulo: 'Atención y Servicio',
    tituloResaltado: 'al Cliente',
    tagline: 'Mejora tu Perfil Profesional',
    taglineEmoji: '👔',
    descripcionHero: 'Domina el manejo de PQRS, comunicación asertiva y clientes difíciles. Certifícate y destaca en cualquier entrevista.',
    precio: 50000,
    precioAnterior: 100000,
    accentHex: '#7c3aed',
    linkPago: 'https://checkout.nequi.wompi.co/l/rxZMK8',
    nombreProducto: 'Cert. Atención al Cliente',
    icono: 'fa-headset',
    iconoSeccion: 'fa-headset',
    beneficios: [
      { icono: 'fa-comments', titulo: 'Comunicación Asertiva', desc: 'Aprende a expresarte con claridad, respeto y empatía hacia el usuario.', bg: 'bg-purple-100', color: 'text-purple-600' },
      { icono: 'fa-exclamation-circle', titulo: 'Manejo de PQRS', desc: 'Protocolos para atender Peticiones, Quejas, Reclamos y Sugerencias.', bg: 'bg-yellow-100', color: 'text-yellow-600' },
      { icono: 'fa-user-tie', titulo: 'Etiqueta y Protocolo', desc: 'Imagen personal, lenguaje corporal y atención telefónica profesional.', bg: 'bg-blue-100', color: 'text-blue-600' },
    ],
    preguntas: [
      { q: '¿Qué significan las siglas PQRS en servicio al cliente?', options: ['Preguntas, Querer, Reír, Soñar', 'Peticiones, Quejas, Reclamos y Sugerencias', 'Problemas Que Requieren Solución'], a: 1 },
      { q: 'Ante un cliente enojado, el primer paso correcto es:', options: ['Discutir para demostrar que estás bien', 'Escuchar activamente y mantener la calma', 'Ignorarlo hasta que se calle'], a: 1 },
      { q: "La 'Comunicación Asertiva' se define como:", options: ['Expresar ideas de forma clara, respetuosa y directa', 'Hablar muy fuerte para ser escuchado', 'Quedarse callado para no molestar'], a: 0 },
      { q: '¿Cuál es la diferencia entre Atención y Servicio?', options: ['No hay diferencia', 'Atención es el proceso (trámite) y Servicio es la experiencia (cómo se sintió)', 'Atención es cobrar y Servicio es regalar cosas'], a: 1 },
      { q: 'La Empatía en el servicio al cliente significa:', options: ['Sentir lástima por el cliente', 'Ponerse en el lugar del cliente para entender su necesidad', 'Darle siempre la razón aunque no la tenga'], a: 1 },
      { q: 'Si no sabes la respuesta a una pregunta del cliente, debes:', options: ['Inventar una respuesta rápida', 'Decirle que busque en Google', 'Admitirlo honestamente y buscar la solución o a alguien que sepa'], a: 2 },
      { q: '¿Por qué es importante la presentación personal?', options: ['Para salir bien en las fotos', 'Porque proyecta la imagen y seriedad de la empresa', 'Solo importa si eres jefe'], a: 1 },
      { q: 'Al finalizar una atención, siempre debes:', options: ['Colgar el teléfono de inmediato', 'Verificar si el cliente quedó satisfecho y despedirse amablemente', 'Pedir propina'], a: 1 },
    ],
  },

  {
    slug: 'auxiliar-de-bodega',
    titulo: 'Auxiliar de Bodega',
    tituloResaltado: 'y Logística',
    tagline: 'Alta Demanda Laboral',
    taglineEmoji: '📦',
    descripcionHero: 'Domina la recepción, almacenamiento, inventarios y despacho. Certifícate y consigue empleo rápido.',
    precio: 50000,
    precioAnterior: 100000,
    accentHex: '#1d4ed8',
    linkPago: 'https://linkdepagospse.rappipay.co/kZYKi5',
    nombreProducto: 'Curso Bodega y Logística',
    icono: 'fa-boxes',
    iconoSeccion: 'fa-dolly',
    beneficios: [
      { icono: 'fa-truck-loading', titulo: 'Recepción y Despacho', desc: 'Verificación de facturas, calidad y cargue de vehículos.', bg: 'bg-blue-100', color: 'text-blue-600' },
      { icono: 'fa-boxes', titulo: 'Control de Inventarios', desc: 'Manejo de Kardex, conteos cíclicos y rotación PEPS.', bg: 'bg-yellow-100', color: 'text-yellow-600' },
      { icono: 'fa-hard-hat', titulo: 'Seguridad Industrial', desc: 'Normativa SST, uso de EPP y levantamiento de cargas.', bg: 'bg-green-100', color: 'text-green-600' },
    ],
    preguntas: [
      { q: '¿Cuál es el primer paso crítico al recibir una mercancía?', options: ['Guardarla rápido', 'Verificar factura vs. físico y estado', 'Firmar sin revisar'], a: 1 },
      { q: 'En el método PEPS (FIFO), ¿qué mercancía debe salir primero?', options: ['La última que llegó', 'La más bonita', 'La primera que entró (más antigua)'], a: 2 },
      { q: "El 'Picking' se refiere al proceso de:", options: ['Limpiar el piso', 'Recolección y alistamiento de pedidos', 'Cargar el camión'], a: 1 },
      { q: '¿Cuáles son EPP indispensables en bodega?', options: ['Gorra y gafas de sol', 'Botas de seguridad y casco', 'Guantes de lana'], a: 1 },
      { q: 'Para levantar una caja pesada del suelo correctamente:', options: ['Doblar la espalda', 'Flexionar las rodillas y espalda recta', 'Hacer fuerza con los brazos'], a: 1 },
      { q: "Un 'Conteo Cíclico' de inventario sirve para:", options: ['Contar toda la bodega una vez al año', 'Verificar referencias específicas periódicamente', 'Eliminar productos'], a: 1 },
      { q: 'Si encuentras un producto averiado, debes:', options: ['Esconderlo', 'Reportarlo como novedad inmediatamente', 'Enviarlo al cliente así'], a: 1 },
      { q: 'El almacenamiento en altura debe hacerse en:', options: ['Racks o estanterías certificadas', 'Apilado en el suelo sin límite', 'Mesas de madera'], a: 0 },
    ],
  },

  {
    slug: 'primeros-auxilios',
    titulo: 'Primeros',
    tituloResaltado: 'Auxilios',
    tagline: 'Requisito para Contratación',
    taglineEmoji: '🚑',
    descripcionHero: 'Certifícate en técnicas de atención de emergencias. RCP, hemorragias, fracturas y más. 100% Válido y Online.',
    precio: 50000,
    accentHex: '#dc2626',
    badgeTexto: 'NUEVO',
    badgeClase: 'bg-red-600',
    linkPago: 'https://checkout.nequi.wompi.co/l/rxZMK8',
    nombreProducto: 'Certificado Primeros Auxilios',
    icono: 'fa-kit-medical',
    iconoSeccion: 'fa-kit-medical',
    beneficios: [
      { icono: 'fa-file-contract', titulo: 'Mejora tu Hoja de Vida', desc: 'Exigido en empresas, colegios, clínicas y brigadas de emergencia.', bg: 'bg-red-100', color: 'text-red-600' },
      { icono: 'fa-heartbeat', titulo: 'Aprende a Salvar Vidas', desc: 'RCP, manejo de hemorragias, fracturas, quemaduras y más.', bg: 'bg-green-100', color: 'text-green-600' },
      { icono: 'fa-laptop', titulo: 'Sin Horarios', desc: 'Estudia y presenta el examen desde tu celular en 20 minutos.', bg: 'bg-purple-100', color: 'text-purple-600' },
    ],
    pixelEnabled: true,
    preguntas: [
      { q: '¿Qué significa RCP?', options: ['Reanimación Cardio-Pulmonar', 'Registro de Control de Pacientes', 'Respuesta Clínica de Primeros Auxilios'], a: 0 },
      { q: '¿A qué velocidad se deben realizar las compresiones torácicas en RCP a un adulto?', options: ['30 compresiones por minuto', '100 a 120 compresiones por minuto', '60 compresiones por minuto'], a: 1 },
      { q: '¿Cuál es lo PRIMERO que se debe hacer al encontrar a una persona inconsciente?', options: ['Darle agua inmediatamente', 'Verificar que el entorno sea seguro y llamar a emergencias', 'Moverla a otro lugar'], a: 1 },
      { q: 'Para detener una hemorragia externa, la medida más efectiva es:', options: ['Aplicar hielo directamente', 'Hacer presión directa y firme sobre la herida con un apósito limpio', 'Lavar la herida con agua caliente'], a: 1 },
      { q: '¿Qué es la Posición Lateral de Seguridad (PLS)?', options: ['Una técnica de masaje cardíaco', 'Una posición para evitar que una persona inconsciente aspire vómito', 'El modo correcto de cargar a un herido'], a: 1 },
      { q: 'Ante una quemadura leve, lo correcto es:', options: ['Aplicar pasta dental o mantequilla', 'Enfriar con agua corriente fría durante 10-20 minutos', 'Reventar las ampollas que se formen'], a: 1 },
      { q: 'Si sospechas que una persona tiene una fractura en el brazo, debes:', options: ['Intentar acomodar el hueso en su lugar', 'Inmovilizar la extremidad sin moverla y buscar ayuda médica', 'Pedir al paciente que mueva el brazo para confirmar la fractura'], a: 1 },
      { q: '¿Cuál es el número de emergencias médicas en Colombia?', options: ['123', '125', '119'], a: 0 },
    ],
  },

  {
    slug: 'informatica-basica',
    titulo: 'Informática',
    tituloResaltado: 'Básica',
    tagline: 'Habilidad Clave para Cualquier Empleo',
    taglineEmoji: '💻',
    descripcionHero: '4 módulos: Sistema Operativo, Windows, Ofimática e Internet. Certificado válido para hoja de vida.',
    precio: 80000,
    accentHex: '#0284c7',
    badgeTexto: 'NUEVO',
    badgeClase: 'bg-sky-600',
    linkPago: 'https://checkout.nequi.wompi.co/l/rxZMK8',
    nombreProducto: 'Curso Informática Básica',
    icono: 'fa-laptop',
    iconoSeccion: 'fa-laptop',
    beneficios: [
      { icono: 'fa-desktop', titulo: 'Sistema Operativo y Windows', desc: 'Manejo del escritorio, archivos, carpetas y configuraciones básicas.', bg: 'bg-sky-100', color: 'text-sky-600' },
      { icono: 'fa-file-word', titulo: 'Ofimática', desc: 'Word, Excel y PowerPoint para el trabajo diario.', bg: 'bg-blue-100', color: 'text-blue-600' },
      { icono: 'fa-globe', titulo: 'Internet y Correo', desc: 'Navegar, buscar información y usar el correo electrónico.', bg: 'bg-indigo-100', color: 'text-indigo-600' },
    ],
    preguntas: [
      { q: '¿Qué es un Sistema Operativo (SO)?', options: ['Un programa para navegar internet', 'El software principal que administra los recursos del computador', 'Un tipo de virus'], a: 1 },
      { q: '¿Cuál es la extensión de un archivo de Word?', options: ['.pdf', '.xlsx', '.docx'], a: 2 },
      { q: "¿Qué significa 'WWW'?", options: ['World Wide Web', 'World Work Web', 'Windows Web World'], a: 0 },
      { q: 'La memoria RAM es:', options: ['El disco donde se guarda información permanentemente', 'La memoria temporal que usa el computador para trabajar', 'El procesador del equipo'], a: 1 },
      { q: '¿Qué hace Ctrl + C en Windows?', options: ['Cerrar el programa', 'Copiar texto o archivo seleccionado', 'Crear una carpeta nueva'], a: 1 },
      { q: '¿Cuál es la función de un navegador web?', options: ['Crear documentos de Word', 'Acceder y explorar páginas de Internet', 'Guardar archivos en el disco duro'], a: 1 },
      { q: "¿Qué es una 'hoja de cálculo'?", options: ['Un documento para escribir textos', 'Una herramienta para organizar datos en filas y columnas (Excel)', 'Un programa para hacer presentaciones'], a: 1 },
      { q: "¿Qué significa 'adjuntar un archivo' en un correo?", options: ['Escribir el texto del correo', 'Enviar un documento o imagen junto al mensaje', 'Responder a todos los destinatarios'], a: 1 },
    ],
  },
];
