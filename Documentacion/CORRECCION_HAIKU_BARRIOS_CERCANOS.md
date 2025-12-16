# 🔧 Corrección: Haiku debe considerar barrios cercanos EN AMBAS DIRECCIONES

**Fecha:** 2025-01-13
**Problema:** Haiku solo considera barrios cercanos en una dirección (Palermo→Belgrano funciona, pero Belgrano→Palermo no)
**Solución:** Agregar instrucción explícita sobre barrios cercanos

---

## 🔍 Problema identificado

### Comportamiento actual:
- ✅ "Busco en Palermo" → Muestra Palermo + Belgrano (barrio vecino)
- ❌ "Busco en Belgrano" → Muestra SOLO Belgrano (no considera Palermo)

### Causa raíz:
El prompt de Haiku no tiene instrucciones sobre considerar ubicaciones cercanas, entonces hace match exacto de la ubicación mencionada.

---

## 🛠️ Solución

### Ubicación del cambio:
**Nodo:** "Preparar Filtrado Haiku" (código JavaScript, línea ~44)

### ANTES:

```javascript
D) CONSULTA ESPECÍFICA CON COINCIDENCIAS
   - Tiene criterios claros (ubicación, tipo, operación, etc.)
   - Hay entre 1-10 propiedades que coinciden bien
   - RESPONDE: IDs de las 3-5 mejores propiedades
```

### DESPUÉS:

```javascript
D) CONSULTA ESPECÍFICA CON COINCIDENCIAS
   - Tiene criterios claros (ubicación, tipo, operación, etc.)
   - Hay propiedades que coinciden bien
   - **IMPORTANTE - UBICACIONES**: Al filtrar por ubicación, considerá también barrios/zonas cercanas:
     * Si pide "Palermo" → incluí también Belgrano, Recoleta (barrios vecinos de CABA)
     * Si pide "Belgrano" → incluí también Palermo, Núñez (barrios vecinos de CABA)
     * Si pide "Ramallo centro" → incluí también Ramallo zona norte, Ramallo zona sur
     * Aplicá este criterio EN AMBAS DIRECCIONES
   - Priorizá las propiedades que coinciden exactamente, pero incluí alternativas cercanas si hay pocas
   - RESPONDE: IDs de las 3-5 mejores propiedades (exactas + cercanas)
```

---

## 📋 Pasos para implementar

### En N8N:

1. **Backup del workflow:**
   - Duplicate workflow antes de modificar
   - Nombrar: "Bot Inmobiliaria - BACKUP [FECHA]"

2. **Editar nodo "Preparar Filtrado Haiku":**
   - Doble click en el nodo
   - Buscar la sección del `haikuPayload`
   - Localizar: `D) CONSULTA ESPECÍFICA CON COINCIDENCIAS`
   - Reemplazar con el texto DESPUÉS mostrado arriba

3. **Guardar:**
   - Click "Save" del nodo
   - Click "Save" del workflow

4. **Activar:**
   - Toggle "Active" en ON

---

## 🧪 Pruebas de verificación

### Test 1: Palermo → Belgrano (ya funcionaba)
**Consulta:** "Busco un departamento en Palermo"
**Resultado esperado:** Muestra Palermo + Belgrano
**Status:** ✅ Ya funcionaba antes

### Test 2: Belgrano → Palermo (el que fallaba)
**Consulta:** "Busco un departamento en Belgrano"
**Resultado esperado:** Muestra Belgrano + Palermo (menciona que es vecino)
**Status:** ⚠️ Debe funcionar después del cambio

### Test 3: Barrio específico de CABA
**Consulta:** "Busco en Recoleta"
**Resultado esperado:** Muestra Recoleta + barrios vecinos (Palermo, Retiro, etc.)
**Status:** ⚠️ Debe funcionar después del cambio

### Test 4: Ciudad del interior (para BBR)
**Consulta:** "Busco en Ramallo"
**Resultado esperado:** Muestra todas las propiedades de Ramallo (centro, norte, sur)
**Status:** ⚠️ Debe funcionar después del cambio

---

## 📊 Cómo funciona el flujo completo

### ANTES de la corrección:
```
Usuario: "Busco en Belgrano"
  ↓
Haiku: Filtra SOLO "Belgrano" (match exacto)
  ↓
Sonnet: Recibe solo propiedades de Belgrano
  ↓
Widget: Muestra solo Belgrano (no hay nada que aclarar)
```

### DESPUÉS de la corrección:
```
Usuario: "Busco en Belgrano"
  ↓
Haiku: Filtra "Belgrano" + barrios cercanos (Palermo, Núñez, etc.)
  ↓
Sonnet: Recibe Belgrano + Palermo → compara ubicaciones
  ↓
Sonnet: "También encontré esta opción en Palermo, un barrio vecino a Belgrano"
  ↓
Widget: Muestra todas las opciones con aclaración
```

---

## ⚠️ Consideraciones importantes

### 1. Balance entre exactitud y flexibilidad:
- Priorizá propiedades con match exacto
- Pero incluí alternativas cercanas para dar más opciones
- Ideal: 60% exactas, 40% cercanas

### 2. Conocimiento geográfico de Haiku:
- Haiku conoce la geografía de CABA (barrios vecinos)
- Puede no conocer ciudades pequeñas del interior
- Para esos casos, usar "zona norte/sur/centro" es más genérico

### 3. Número de propiedades:
- Si hay 5+ propiedades exactas → priorizar esas
- Si hay <3 propiedades exactas → agregar cercanas hasta llegar a 5

---

## ✅ Resultado esperado

Una vez aplicado el cambio:

1. **Búsquedas bidireccionales:** Palermo↔Belgrano funcionan en ambas direcciones
2. **Más opciones al usuario:** Siempre muestra 3-5 propiedades relevantes
3. **Mejor experiencia:** Usuario ve alternativas cercanas aunque no haya en su barrio exacto
4. **Aclaraciones claras:** Sonnet menciona cuando es barrio vecino

---

**Autor:** Claude Code
**Fecha creación:** 2025-01-13
**Última actualización:** 2025-01-13
