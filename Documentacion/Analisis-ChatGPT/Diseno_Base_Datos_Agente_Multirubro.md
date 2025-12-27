# 🗄️ Diseño de Base de Datos — Agente Comercial Inteligente Multirubro (SaaS)
## (Versión extendida con Follow-up y Contexto Conversacional)

---

## 🧠 Concepto clave
El **follow-up** permite que el bot recuerde el contexto de una conversación.
Se implementa mediante:
- historial completo (`mensajes`)
- memoria resumida (`contextos_conversacion`)
- reglas del plan (`nivel_followup`)

---

## 🏢 empresas
```sql
CREATE TABLE empresas (
    id UUID PRIMARY KEY,
    nombre VARCHAR(100),
    rubro_id UUID,
    plan_id UUID,
    prompt_empresa TEXT,
    activa BOOLEAN DEFAULT true,
    fecha_alta TIMESTAMP,
    fecha_baja TIMESTAMP
);
```

---

## 🏷️ rubros
```sql
CREATE TABLE rubros (
    id UUID PRIMARY KEY,
    nombre VARCHAR(50),
    descripcion TEXT,
    prompt_rubro TEXT,
    prompt_restricciones TEXT,
    prompt_ejemplos TEXT,
    activo BOOLEAN DEFAULT true
);
```

---

## 💳 planes
```sql
CREATE TABLE planes (
    id UUID PRIMARY KEY,
    nombre VARCHAR(50),
    nivel_followup INT,
    max_tokens_mensuales INT,
    modelo_ia VARCHAR(50),
    permite_historial BOOLEAN,
    canales_habilitados JSONB,
    activo BOOLEAN
);
```

---

## 👤 usuarios_finales
```sql
CREATE TABLE usuarios_finales (
    id UUID PRIMARY KEY,
    empresa_id UUID,
    canal VARCHAR(30),
    identificador_externo VARCHAR(100),
    fecha_alta TIMESTAMP
);
```

---

## 💬 conversaciones
```sql
CREATE TABLE conversaciones (
    id UUID PRIMARY KEY,
    usuario_id UUID,
    empresa_id UUID,
    canal VARCHAR(30),
    fecha_inicio TIMESTAMP,
    fecha_fin TIMESTAMP
);
```

---

## ✉️ mensajes
```sql
CREATE TABLE mensajes (
    id UUID PRIMARY KEY,
    conversacion_id UUID,
    rol VARCHAR(20),
    contenido TEXT,
    tokens_usados INT,
    fecha TIMESTAMP
);
```

---

## 🧠 contextos_conversacion
```sql
CREATE TABLE contextos_conversacion (
    id UUID PRIMARY KEY,
    conversacion_id UUID,
    empresa_id UUID,
    nivel_followup INT,
    contexto_resumido TEXT,
    tokens_contexto INT,
    ultima_actualizacion TIMESTAMP
);
```

---

## 🧠 prompts
```sql
CREATE TABLE prompts (
    id UUID PRIMARY KEY,
    tipo VARCHAR(30),
    referencia_id UUID,
    contenido TEXT,
    version INT,
    activo BOOLEAN,
    fecha_creacion TIMESTAMP
);
```

---

## 📦 items_rubro
```sql
CREATE TABLE items_rubro (
    id UUID PRIMARY KEY,
    empresa_id UUID,
    tipo VARCHAR(30),
    datos JSONB,
    activo BOOLEAN
);
```

---

## 📊 metricas
```sql
CREATE TABLE metricas (
    id UUID PRIMARY KEY,
    empresa_id UUID,
    fecha DATE,
    tokens_usados INT,
    consultas INT
);
```

---

## 🎯 Conclusión
Modelo preparado para SaaS multirubro con follow-up controlado.
