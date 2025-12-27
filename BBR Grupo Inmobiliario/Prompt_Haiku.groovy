// ============================================
// PREPARAR HAIKU TODO-EN-UNO - PLAN BÁSICO
// Filtrado + Respuesta en una sola llamada
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
  
  // Construir objeto con toda la info necesaria
  const propInfo = {
    id: id,
    tipo: p.tipo || 'Propiedad',
    operacion: p.operacion || 'Venta',
    titulo: p.titulo || `${p.tipo} en ${p.direccion?.barrio || 'Buenos Aires'}`,
    ubicacion: p.direccion?.barrio || p.barrio || 'Buenos Aires',
    precio: p.precio?.valor || p.precio || 'Consultar',
    moneda: p.precio?.moneda || 'USD',
    expensas: p.expensas?.valor || null,
    ambientes: p.caracteristicas?.ambientes || p.ambientes || null,
    dormitorios: p.caracteristicas?.dormitorios || p.dormitorios || null,
    banos: p.caracteristicas?.banos || p.banos || null,
    superficie: p.caracteristicas?.superficie_total || p.superficie || null,
    cochera: p.detalles?.cochera || p.cochera || false,
    balcon: p.detalles?.balcon || p.balcon || false,
    jardin: p.detalles?.jardin || p.jardin || false,
    descripcion: p.descripcion || ''
  };

  // ✅ AGREGAR FOTOS CON ESTRUCTURA COMPLETA (igual que Haiku+Sonnet)
  if (p.fotos && p.fotos.urls && p.fotos.urls.length > 0) {
    propInfo.fotos = {
      cantidad: p.fotos.cantidad || p.fotos.urls.length,
      urls: p.fotos.urls,
      destacados: p.fotos.destacados || []
    };
  }

  return propInfo;
});

// 4. CONSTRUIR PAYLOAD PARA HAIKU
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

A) SALUDO SIMPLE(sin búsqueda específica):
   → Respondé con saludo breve y preguntá qué busca

B) SI BUSCA ALGO QUE NO EXISTE EN EL CATÁLOGO:
   → Informá que no hay propiedades con esas características

C) SI ES MUY GENÉRICA (sin ubicación, tipo, ni operación):
   → Pedí más detalles (ubicación, tipo, operación)

D) SI TIENE CRITERIOS CLAROS Y HAY COINCIDENCIAS:
   → Mostrá las 3-5 propiedades más relevantes

⚠️ MUY IMPORTANTE:
- NO expliques tu razonamiento
- NO digas "esto es tipo A/B/C/D"
- NO digas "Entendido, voy a..."
- SOLO respondé directamente según el formato de abajo

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

• ¿En qué zona buscás?
• ¿Para alquilar o comprar?
• ¿Qué tipo de propiedad?
---

🔹 FORMATO PARA PROPIEDADES (Tipo D):

ESTRUCTURA:
1. Línea intro: "Encontré [X] [tipo de propiedad] en [ubicación]:"
2. Línea vacía
3. Por cada propiedad, incluí OBLIGATORIAMENTE estas líneas (en este orden):

🏢 [Título completo]
📍 Calle + Barrio
💰 [Precio/mes o precio total] + expensas (si es alquiler)
🛏️ [N] ambientes, [N] dormitorios, [N] baños
📏 [N] m²

Luego agregá SOLO si la propiedad tiene:
🚗 Cochera
🌿 Balcón/Jardín/Terraza
✨ Piscina/Parrilla/etc
   - 📸 [TODAS las URLs de fotos] (si tiene fotos)
   - Línea vacía
4. CIERRE OBLIGATORIO (copiar exactamente):
  "¿Alguna de estas propiedades te interesa? Podés:\n✅ Dejar tus datos de contacto\n🔍 Ver otras opciones"

REGLAS IMPORTANTES:

1. **NO EXPLIQUES TU RAZONAMIENTO**:
   - NO digas "Entendido", "Para esta consulta", "Corresponde tipo X", etc.
   - NO expliques por qué elegiste una respuesta u otra
   - SOLO respondé directamente lo que el usuario necesita
   - Las clasificaciones internas NO deben aparecer en tu respuesta

2. **FOTOS**: Si la propiedad tiene fotos, incluí TODAS las URLs en UNA sola línea separadas por espacios
   Formato: 📸 [URL1] [URL2] [URL3]

3. **UBICACIONES**: NO compares barrios ni sugieras "cercanos"
   Solo mostrá propiedades que coincidan exactamente con lo pedido

4. **LÍMITE**: Máximo 5 propiedades por respuesta

5. **IDIOMA**: Siempre en español

6. **TONO**: Directo y simple, sin mucha narrativa

7. **SALUDOS MIXTOS**: Si el usuario dice "hola" + consulta específica (ej: "hola busco casa"),
    saluda brevemente y tratalo como Tipo D (consulta específica).

8. **SALTOS DE LÍNEA**: Usa saltos de línea REALES entre las opciones del cierre
    NO escribas el texto "\n" literalmente - eso es un error
    Simplemente presioná Enter para separar cada línea

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