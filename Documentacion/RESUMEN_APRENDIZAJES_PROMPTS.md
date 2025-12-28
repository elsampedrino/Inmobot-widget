# 📚 Aprendizajes Clave: Prompts de Chatbot Inmobiliario

**Fecha:** 28 de Diciembre 2025

---

## 🎯 10 Lecciones Principales

### 1️⃣ **Reglas Explícitas con Ejemplos Concretos**

```
✅ BIEN:
"D) CONSULTA CON CRITERIO:
Si menciona tipo u operación, SIEMPRE mostrar propiedades.
Ejemplos: 'busco departamento', 'tenes casas?', 'algo para alquilar'"

❌ MAL:
"D) Si tiene criterios claros, mostrar propiedades"
```

**Por qué:** Los LLMs necesitan ejemplos para entender límites.

---

### 2️⃣ **Prohibiciones Explícitas**

```
PROHIBICIÓN ABSOLUTA:
- NO expliques tu razonamiento
- NO uses "Interpreto esto como..."
- NO digas "Corresponde al tipo..."
```

**Por qué:** Decir "NO hagas X" previene comportamientos no deseados.

---

### 3️⃣ **Normalización de Lenguaje Natural**

```
EQUIVALENCIAS:
- departamento = depto = dpto
- alquilar = rentar = alquiler
- casas → casa (singular)
```

**Por qué:** Los usuarios usan vocabulario variado.

---

### 4️⃣ **Formato Compacto para Filtrado**

```javascript
// Catálogo completo: ~15,000 tokens
JSON.stringify(propiedades)

// Catálogo compacto: ~500 tokens
"PROP-001|Casa|Venta|USD139K|Ramallo|3amb|2dorm"
```

**Por qué:** Reduce costos en workflows de dos etapas.

---

### 5️⃣ **Cantidad Explícita en Resultados**

```
✅ "Tengo 3 casas disponibles:"
❌ "Tengo casas disponibles:"
```

**Por qué:** Mejora la experiencia del usuario.

---

### 6️⃣ **Ordenamiento Pre-Prompt**

```javascript
// Ordenar ANTES de enviar al LLM
const sorted = props.sort((a,b) => a.precio - b.precio);
const top5 = sorted.slice(0, 5);
```

**Por qué:** Reduce complejidad del prompt.

---

### 7️⃣ **Sistema Dual: Filtro + Respuesta**

```
Haiku (Filtro)  →  GREETING | NO_MATCH | TOO_GENERIC | IDs
                ↓
Sonnet (Respuesta)  →  Mensaje personalizado multiidioma
```

**Por qué:** Optimiza costo/calidad (70% ahorro).

---

### 8️⃣ **Fotos en Una Línea**

```
✅ 📸 url1.jpg url2.jpg url3.jpg
❌ 📸 url1.jpg
   📸 url2.jpg
```

**Por qué:** Facilita parseo en widgets.

---

### 9️⃣ **Mapeo Correcto de Datos**

```javascript
// ❌ Asumir
cochera: p.detalles.cochera

// ✅ Validar
cochera: Array.isArray(p.detalles) ? p.detalles.includes('cochera') : false
```

**Por qué:** Las estructuras JSON varían entre fuentes.

---

### 🔟 **Detección Automática de Idioma**

```
"Detectá el idioma de la consulta.
Respondé en el mismo idioma: ES, EN o PT"
```

**Por qué:** Sonnet puede hacerlo sin configuración adicional.

---

## 🔑 Patrón de Prompt Exitoso

```javascript
// 1. CONTEXTO
"Sos un asistente inmobiliario para Argentina"

// 2. DATOS
CONSULTA: "${consulta}"
CATÁLOGO: ${JSON.stringify(propiedades)}

// 3. NORMALIZACIÓN
EQUIVALENCIAS:
- depto = departamento
- alquilar = rentar

// 4. CLASIFICACIÓN
A) SALUDO → formato X
B) SIN RESULTADOS → formato Y
C) GENÉRICA → formato Z
D) CON CRITERIO → formato W

// 5. REGLAS
PRIORIDAD: Si menciona tipo u operación → SIEMPRE Tipo D
PROHIBIDO: NO expliques razonamiento

// 6. FORMATO
ESTRUCTURA OBLIGATORIA:
1. Intro con cantidad
2. Detalles de propiedades
3. Fotos en una línea

// 7. PROHIBICIONES
NO uses frases como "Interpreto...", "Corresponde a..."
```

---

## 📊 Resultados Medibles

### Antes de las Mejoras:
- ❌ "busco departamento para alquilar" → Saludo genérico
- ❌ "tenes casas?" → Botones de opciones
- ⚠️ Estructura incorrecta (cochera, expensas)

### Después de las Mejoras:
- ✅ "busco departamento para alquilar" → Muestra PROP-027
- ✅ "tenes casas?" → Lista todas las casas por precio
- ✅ Todos los campos mapeados correctamente

**Mejora de precisión:** ~95% de consultas específicas resueltas correctamente

---

## 🎓 Aplicable a Otros Dominios

Estos principios funcionan para cualquier chatbot de búsqueda:

- 🏥 **Salud:** Buscar médicos, especialidades, horarios
- 🍕 **Restaurantes:** Buscar por cocina, ubicación, precio
- 🚗 **Autos:** Buscar por marca, modelo, año
- 📚 **Educación:** Buscar cursos, nivel, duración
- ✈️ **Turismo:** Buscar destinos, fechas, presupuesto

**Patrón universal:**
1. Normalizar lenguaje
2. Clasificar intención (A/B/C/D)
3. Reglas explícitas con ejemplos
4. Prohibir meta-explicaciones
5. Formato estructurado
6. Pre-procesamiento de datos

---

## 🔄 Evolución del Prompt

### Versión 1 (Inicial)
```
"Filtra propiedades según la consulta y responde"
```
**Problema:** Muy ambiguo

---

### Versión 2 (Con Categorías)
```
A) Saludo
B) Sin coincidencias
C) Genérica
D) Específica
```
**Problema:** Sin ejemplos concretos

---

### Versión 3 (Con Ejemplos)
```
A) SALUDO: "hola", "buenos días"
D) ESPECÍFICA: "busco departamento", "tenes casas?"
```
**Problema:** Aún confunde casos límite

---

### Versión 4 (Con Reglas de Prioridad) ⭐
```
REGLA ABSOLUTA:
Si menciona tipo u operación → SIEMPRE Tipo D

PROHIBIDO:
- NO expliques razonamiento
- NO uses "Interpreto..."

EJEMPLOS:
✅ "busco departamento" → Tipo D
✅ "tenes casas?" → Tipo D
❌ "qué tenés?" → Tipo C
```
**Resultado:** ~95% de precisión

---

## 💡 Insights Finales

1. **Más reglas ≠ Mejor prompt**
   - Lo importante es la claridad, no la cantidad

2. **Ejemplos > Descripciones**
   - "Ejemplo: 'busco casa' → Tipo D" mejor que "consultas sobre tipo"

3. **Prohibiciones son tan importantes como instrucciones**
   - "NO hagas X" previene comportamientos emergentes

4. **Pre-procesar > Delegar al LLM**
   - Ordenar, filtrar, limitar ANTES del prompt

5. **Testing iterativo**
   - Cada mejora basada en casos reales fallidos

6. **Sistema dual optimiza costo/calidad**
   - Filtro barato + Respuesta premium = 70% ahorro

---

**Actualizado:** 28 de Diciembre 2025
