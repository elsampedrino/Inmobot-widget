# 📸 Corrección: Mostrar TODAS las fotos en el widget

**Fecha:** 2025-01-13
**Problema detectado:** El bot solo muestra 1 foto por propiedad
**Causa:** El prompt de Sonnet solo pide la primera foto
**Solución:** Modificar prompt para incluir todas las URLs

---

## 🔍 Diagnóstico

### Estado actual del widget:
✅ **El widget YA está preparado para mostrar múltiples fotos**
- Tiene un regex que detecta TODAS las URLs de imágenes en el texto
- Crea una galería automática con todas las fotos encontradas
- Permite hacer click para ampliar

### Problema en N8N:
❌ **El prompt de Sonnet solo incluye la primera foto**
- Ubicación: Nodo "Preparar Respuesta Sonnet" (línea ~99 del workflow)
- Instrucción actual: `"📸 Ver fotos: [URL de la primera foto]"`
- Resultado: Solo se envía 1 URL → widget solo muestra 1 foto

---

## 🛠️ Solución: Actualizar prompt de Sonnet

### Ubicación en N8N:
1. Abrir workflow: **"Bot Inmobiliaria - Haiku + Sonnet (CON MANEJO DE ERRORES)"**
2. Buscar nodo: **"Preparar Respuesta Sonnet"** (nodo de código JavaScript)
3. Dentro del código, buscar la variable `sonnetPayload`
4. Localizar la sección de instrucciones para fotos

### ANTES (línea ~99):

```javascript
2. **Por cada propiedad:**
   - Título descriptivo con emoji apropiado (🏠 casa, 🏢 depto, 🏪 local)
   - Características principales en formato natural (NO uses listas de bullets)
   - Precio con formato argentino (ej: USD 950/mes + $85.000 expensas)
   - **MUY IMPORTANTE - FOTOS**: Si la propiedad tiene fotos, incluí al final:
     "📸 Ver fotos: [URL de la primera foto]"
```

### DESPUÉS (reemplazar con esto):

```javascript
2. **Por cada propiedad:**
   - Título descriptivo con emoji apropiado (🏠 casa, 🏢 depto, 🏪 local)
   - Características principales en formato natural (NO uses listas de bullets)
   - Precio con formato argentino (ej: USD 950/mes + $85.000 expensas)
   - **IMPORTANTE - UBICACIÓN**: Compará la ubicación de cada propiedad con lo que pidió el usuario en la consulta original.
     Si la ubicación es diferente pero cercana, mencionalo ANTES de mostrar esa propiedad.
     Esto aplica EN AMBAS DIRECCIONES y para cualquier ubicación:
     * Si pidió "Palermo" pero mostrás Belgrano → "También encontré esta opción en Belgrano, un barrio vecino a Palermo"
     * Si pidió "Belgrano" pero mostrás Palermo → "También encontré esta opción en Palermo, un barrio vecino a Belgrano"
     * Si pidió "centro de Ramallo" pero mostrás "zona norte de Ramallo" → mencionar la diferencia
     * SIEMPRE compará: consulta vs ubicación real de la propiedad
   - **MUY IMPORTANTE - FOTOS**: Si la propiedad tiene fotos, incluí TODAS las URLs al final en UNA SOLA LÍNEA separadas por espacios.
     Formato: 📸 [URL_1] [URL_2] [URL_3]
     Ejemplo: "📸 https://res.cloudinary.com/.../foto01.jpg https://res.cloudinary.com/.../foto02.jpg https://res.cloudinary.com/.../foto03.jpg"
```

---

## 📋 Pasos para aplicar el cambio:

### En N8N:

1. **Hacer backup del workflow actual:**
   - Click derecho en el workflow → "Duplicate"
   - Renombrar copia: "Bot Inmobiliaria - BACKUP [FECHA]"

2. **Editar el nodo "Preparar Respuesta Sonnet":**
   - Hacer doble click en el nodo
   - Buscar la sección del prompt (variable `sonnetPayload`)
   - Localizar: `**MUY IMPORTANTE - FOTOS**`
   - Reemplazar el texto según lo indicado arriba

3. **Guardar cambios:**
   - Click en "Save" del nodo
   - Click en "Save" del workflow (arriba a la derecha)

4. **Activar el workflow:**
   - Toggle "Active" en ON
   - Verificar que el webhook esté respondiendo

### Prueba de verificación:

**Consulta de prueba:**
```
Busco un departamento de 2 ambientes en Palermo
```

**Resultado esperado:**
- El bot debe responder con propiedades
- Cada propiedad debe mostrar varias fotos (no solo 1)
- Las fotos deben aparecer como thumbnails clickeables
- Al hacer click, se debe abrir la foto en tamaño completo

---

## 🔧 Alternativa (si hay problemas):

Si el formato de múltiples líneas genera problemas, podés usar este formato alternativo:

```javascript
   - **MUY IMPORTANTE - FOTOS**: Si la propiedad tiene fotos, incluí TODAS las URLs en una línea separadas por espacios:
     "📸 [URL_1] [URL_2] [URL_3]"
```

El widget detectará las URLs igual porque usa un regex global que busca todas las coincidencias.

---

## 📊 Datos técnicos

### Estructura de fotos en el JSON:
```json
"fotos": {
  "cantidad": 3,
  "urls": [
    "https://res.cloudinary.com/.../foto01.jpg",
    "https://res.cloudinary.com/.../foto02.jpg",
    "https://res.cloudinary.com/.../foto03.jpg"
  ],
  "destacados": []
}
```

### Regex del widget que detecta imágenes:
```javascript
const imageRegex = /(https?:\/\/[^\s]+\.(?:jpg|jpeg|png|gif|webp))/gi;
```

Este regex:
- ✅ Detecta URLs que empiecen con `http://` o `https://`
- ✅ Detecta extensiones: `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`
- ✅ Flag `g` (global): encuentra TODAS las coincidencias, no solo la primera
- ✅ Flag `i` (insensitive): no distingue mayúsculas/minúsculas

---

## ✅ Resultado final

Una vez aplicado el cambio:

1. **El bot enviará todas las URLs de fotos** en el texto de respuesta
2. **El widget detectará automáticamente todas las URLs** con el regex
3. **Se mostrará una galería con todas las fotos** como thumbnails
4. **El usuario podrá ver todas las fotos** de cada propiedad

**Beneficios:**
- ✨ Mejor experiencia de usuario
- 🖼️ El cliente ve todas las fotos sin tener que pedirlas
- 📱 Funciona perfecto en mobile y desktop
- 🚀 No requiere cambios en el widget (ya está listo)

---

## 📝 Notas adicionales

- Esta corrección **NO afecta** el funcionamiento del filtrado Haiku
- **NO afecta** el manejo de errores
- **NO afecta** el sistema de idiomas (ES/EN/PT)
- Solo mejora la **presentación visual** de las propiedades

**Autor:** Claude Code
**Fecha creación:** 2025-01-13
**Última actualización:** 2025-01-13