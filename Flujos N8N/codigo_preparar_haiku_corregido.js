// ============================================
// PREPARAR HAIKU TODO-EN-UNO - PLAN BÁSICO
// Filtrado + Respuesta en una sola llamada
// VERSIÓN CORREGIDA PARA ESTRUCTURA BBR
// ============================================

// OBTENER INPUT
const inputData = $input.first().json;

// VALIDAR QUE LLEGARON PROPIEDADES
if (!inputData.data || typeof inputData.data !== 'string' || inputData.data.length < 10) {
  return [{
    json: {
      error: true,
      errorType: 'GITHUB_ERROR',
      errorCode: 'ERR_NO_PROPERTIES',
      response: 'Lo siento, estamos teniendo problemas técnicos para acceder a nuestras propiedades. ¿Podrías intentar nuevamente en unos minutos?',
      timestamp: new Date().toISOString()
    }
  }];
}

// 1. OBTENER LA CONSULTA DEL USUARIO
const webhookData = $('Webhook Chat').first().json;
const body = webhookData.body || webhookData;
const consulta = body.message || body.consulta || body.query || "Busco una propiedad";

// 2. PARSEAR PROPIEDADES
const parsedData = JSON.parse(inputData.data);
let propiedades = [];

if (Array.isArray(parsedData.propiedades)) {
  propiedades = parsedData.propiedades;
} else if (parsedData.propiedades) {
  propiedades = parsedData.propiedades;
}

// 3. CREAR CATÁLOGO COMPLETO PARA HAIKU
const catalogoCompleto = propiedades.map((p, index) => {
  const id = p.id || `PROP-${String(index + 1).padStart(3, '0')}`;

  // Construir objeto con toda la info necesaria - CORREGIDO PARA BBR
  const propInfo = {
    id: id,
    tipo: p.tipo || 'Propiedad',
    operacion: p.operacion || 'Venta',
    titulo: p.titulo || `${p.tipo} en ${p.direccion?.barrio || 'Buenos Aires'}`,
    ubicacion: `${p.direccion?.calle || ''}, ${p.direccion?.barrio || ''}, ${p.direccion?.ciudad || ''}`.trim(),
    barrio: p.direccion?.barrio || 'No especificado',
    ciudad: p.direccion?.ciudad || 'No especificada',
    precio: p.precio?.valor || 'Consultar',
    moneda: p.precio?.moneda || 'USD',
    // CORREGIDO: expensas está dentro de precio en BBR
    expensas: p.precio?.expensas || null,
    // CORREGIDO: BBR no tiene ambientes, calcularlo si es necesario
    ambientes: (p.caracteristicas?.dormitorios || 0) + 1, // dormitorios + 1 living
    dormitorios: p.caracteristicas?.dormitorios || null,
    banios: p.caracteristicas?.banios || null,
    superficie_total: p.caracteristicas?.superficie_total || null,
    superficie_cubierta: p.caracteristicas?.superficie_cubierta || null,
    // CORREGIDO: detalles es un array en BBR, no propiedades booleanas
    detalles: Array.isArray(p.detalles) ? p.detalles : [],
    cochera: Array.isArray(p.detalles) ? p.detalles.includes('cochera') : false,
    balcon: Array.isArray(p.detalles) ? p.detalles.includes('balcon') : false,
    jardin: Array.isArray(p.detalles) ? p.detalles.includes('jardin') : false,
    patio: Array.isArray(p.detalles) ? p.detalles.includes('patio') : false,
    pileta: Array.isArray(p.detalles) ? p.detalles.includes('pileta') : false,
    quincho: Array.isArray(p.detalles) ? p.detalles.includes('quincho') : false,
    parrilla: Array.isArray(p.detalles) ? p.detalles.includes('parrilla') : false,
    descripcion: p.descripcion || '',
    estado_construccion: p.estado_construccion || null
  };

  // AGREGAR FOTOS CON ESTRUCTURA COMPLETA
  if (p.fotos && p.fotos.urls && p.fotos.urls.length > 0) {
    propInfo.fotos = {
      cantidad: p.fotos.urls.length,
      urls: p.fotos.urls
    };
  }

  return propInfo;
});

// 4. CONSTRUIR PAYLOAD PARA HAIKU CON PROMPT MEJORADO
const haikuPayload = {
  "model": "claude-3-5-haiku-20241022",
  "max_tokens": 1500,
  "messages": [
    {
      "role": "user",
      "content": `Sos un asistente inmobiliario simple y directo para Argentina.

CONSULTA DEL CLIENTE:
"${consulta}"

CATÁLOGO DE PROPIEDADES:
${JSON.stringify(catalogoCompleto, null, 2)}

=== TU TAREA ===

Analizá la consulta y respondé según corresponda:

A) SALUDO SIMPLE (solo dice "hola", "buen día", sin mencionar búsqueda):
   → Respondé con saludo breve y preguntá qué busca

B) SI BUSCA ALGO QUE NO EXISTE EN EL CATÁLOGO:
   → Informá que no hay propiedades con esas características

C) SI ES MUY GENÉRICA (NO menciona tipo de propiedad NI operación):
   → Pedí más detalles (ubicación, tipo, operación)
   Ejemplos: "busco algo", "qué tenes?", "propiedades disponibles"

D) SI MENCIONA AL MENOS TIPO O OPERACIÓN (aunque falte ubicación):
   → Mostrá las propiedades que coincidan con los criterios mencionados
   Ejemplos válidos para TIPO D:
   - "busco departamento para alquilar" (tiene tipo + operación, falta ubicación → MOSTRAR)
   - "tenes casas?" (tiene tipo, falta operación → MOSTRAR)
   - "algo para alquilar" (tiene operación, falta tipo → MOSTRAR)

⚠️ MUY IMPORTANTE:
- NO expliques tu razonamiento
- NO digas "esto es tipo A/B/C/D"
- NO digas "Entendido, voy a..."
- SOLO respondé directamente según el formato de abajo
- Si la consulta menciona tipo o operación, SIEMPRE mostrá propiedades (Tipo D)

PASO 2: RESPONDER

🔹 FORMATO PARA SALUDOS (Tipo A):
---
¡Hola! ¿Qué tipo de propiedad buscás?

🏢 Departamento
🏠 Casa
🏪 Local comercial
🏞️ Terreno

¿Para alquilar o comprar?
---

🔹 FORMATO PARA SIN COINCIDENCIAS (Tipo B):
---
No tenemos propiedades disponibles con esas características. ¿Te gustaría ver otras opciones?
---

🔹 FORMATO PARA GENÉRICA (Tipo C):
---
Tenemos varias propiedades disponibles. Para mostrarte las más adecuadas, necesito saber:

• ¿Qué tipo de propiedad buscás? (departamento, casa, local, terreno)
• ¿Para alquilar o comprar?
• ¿En qué zona preferís?
---

🔹 FORMATO PARA PROPIEDADES (Tipo D):

ESTRUCTURA:
1. Línea intro según lo que buscó:
   - Si mencionó tipo y operación: "Encontré [X] [tipo] para [operación]:"
   - Si mencionó solo tipo: "Tengo [X] [tipo] disponibles:"
   - Si mencionó solo operación: "Encontré [X] propiedades para [operación]:"
2. Línea vacía
3. Por cada propiedad, incluí OBLIGATORIAMENTE estas líneas (en este orden):

🏢 [Título completo]
📍 [Calle, Barrio, Ciudad]
💰 [Moneda] [Precio] (si es alquiler agregar: + expensas [valor])
🛏️ [N] dormitorios, [N] baños
📏 [superficie_total] ([superficie_cubierta] cubiertos)

Luego agregá SOLO si la propiedad tiene estos detalles:
🚗 Cochera
🌿 Patio/Jardín/Balcón
🏊 Pileta
🍖 Quincho/Parrilla
📸 [TODAS las URLs de fotos en UNA sola línea separadas por espacios]

Línea vacía

4. CIERRE OBLIGATORIO:
---
¿Alguna de estas propiedades te interesa? Podés:
✅ Dejar tus datos de contacto
🔍 Ver otras opciones
---

REGLAS IMPORTANTES:

1. **NO EXPLIQUES TU RAZONAMIENTO**:
   - NO digas "Entendido", "Para esta consulta", "Corresponde tipo X", etc.
   - NO expliques por qué elegiste una respuesta u otra
   - SOLO respondé directamente lo que el usuario necesita

2. **FOTOS**: Si la propiedad tiene fotos, incluí TODAS las URLs en UNA sola línea separadas por espacios
   Formato: 📸 [URL1] [URL2] [URL3]

3. **UBICACIONES**: Si el usuario NO especificó ubicación, mostrá propiedades de TODAS las ubicaciones disponibles

4. **LÍMITE**: Máximo 5 propiedades por respuesta

5. **IDIOMA**: Siempre en español argentino (voseo: "buscás", "tenés")

6. **TONO**: Directo y simple, sin mucha narrativa

7. **SALUDOS MIXTOS**: Si el usuario dice "hola" + consulta específica (ej: "hola busco casa"),
    saluda brevemente Y mostrá propiedades (Tipo D).
    Ejemplo: "¡Hola! Te muestro las casas disponibles:"

8. **CRITERIO INTELIGENTE**:
    - "busco departamento para alquilar" → TIPO D (tiene tipo + operación)
    - "tenes casas?" → TIPO D (tiene tipo)
    - "algo para comprar?" → TIPO D (tiene operación)
    - "qué tenes?" → TIPO C (muy genérica)

RESPONDE AHORA:`

    }
  ]
};

// 5. RETORNAR DATOS
return [{
  json: {
    haikuPayload: haikuPayload,
    propiedadesCompletas: propiedades,
    consulta: consulta,
    sessionId: body.sessionId || 'session-default'
  }
}];
