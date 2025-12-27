# Caso de Prueba – Inmobiliaria con Follow-up Inteligente

## 1. Contexto General
Este documento describe un caso de uso completo del **Agente Comercial Inteligente Multirubro**, aplicado al rubro **Inmobiliario**, integrando:
- conversación asistida por IA
- gestión de leads
- almacenamiento de contexto
- follow-up automático e inteligente

El objetivo es demostrar el funcionamiento del modelo extremo a extremo, sin entrar en código.

---

## 2. Rubro
**Rubro:** Inmobiliaria  

**Necesidades típicas del rubro:**
- Responder consultas 24/7
- Mostrar propiedades según filtros
- Captar datos de contacto
- Hacer seguimiento sin depender de tareas manuales

---

## 3. Empresa
**Nombre:** Inmobiliaria Ejemplo SRL  
**Plan contratado:** Profesional  
**Canales habilitados:** Web + Telegram  
**Follow-up habilitado:** Sí  
**Horario humano:** Lunes a Viernes de 9 a 18 hs  

Fuera de horario, el agente opera de forma autónoma.

---

## 4. Activos del Negocio
### 4.1 Propiedad (ejemplo)
- ID Propiedad: 101
- Tipo: Departamento
- Operación: Alquiler
- Ambientes: 2
- Zona: Palermo
- Precio: $600.000
- Mascotas: Sí
- Estado: Disponible

---

## 5. Lead
### Lead inicial
- ID Lead: 9001
- Nombre: Juan Pérez
- Canal: Web
- Teléfono: +54 9 11 xxxx xxxx
- Estado: Nuevo
- Fuente: Formulario Web

---

## 6. Conversación Inicial
**Usuario:**  
> Hola, estoy buscando un departamento de 2 ambientes en Palermo que acepten mascotas.

**IA (agente):**  
> ¡Hola Juan! 😊  
> Tengo una opción en Palermo, 2 ambientes, acepta mascotas y está en $600.000.  
> ¿Querés que te pase más detalles o coordinar una visita?

### Datos que se guardan:
- Conversación
- Intención detectada: alquiler
- Filtros aplicados
- Propiedad asociada
- Lead actualizado

---

## 7. Evaluación de Follow-up
La IA evalúa automáticamente:
- Lead mostró interés ✔
- No se concretó acción (visita) ❌
- Follow-up permitido ✔
- Plan lo habilita ✔

➡️ Se decide generar follow-up automático.

---

## 8. Follow-up (Detalle)
### Registro generado
- followup_id: 501
- lead_id: 9001
- tipo: recordatorio_visita
- mensaje_sugerido:
  > "Hola Juan 👋 ¿Querías coordinar una visita al depto de Palermo que vimos ayer?"
- estado: pendiente
- fecha_programada: +24 hs
- canal: mismo canal del lead

---

## 9. Ejecución del Follow-up
A las 24 hs el sistema envía el mensaje.

**Bot / IA:**  
> Hola Juan 👋 ¿Querías coordinar una visita al depto de Palermo que te comenté ayer?

**Usuario:**  
> Sí, el sábado a la mañana.

### Resultado:
- Follow-up → completado
- Lead → Calificado
- Acción → Derivar a humano / agenda

---

## 10. Flujo Técnico Simplificado
1. Usuario inicia conversación
2. API recibe mensaje + contexto
3. IA filtra datos y responde
4. Se guarda interacción
5. Se evalúa follow-up
6. n8n programa evento
7. IA envía follow-up
8. Usuario responde
9. Lead cambia de estado

---

## 11. Rol de n8n
n8n no contiene la lógica de negocio principal.

Su función es:
- Orquestar eventos
- Programar follow-ups
- Enviar mensajes
- Integrarse con canales externos

La inteligencia vive en la API y la base de datos.

---

## 12. Beneficios del Modelo
- Multirubro real
- Escalable por planes
- Menor costo de IA
- Contexto persistente
- Experiencia humana sin intervención constante

---

## 13. Conclusión
Este caso demuestra que:
- Un solo core puede atender múltiples rubros
- El follow-up es clave para conversión
- La IA no reemplaza al humano, lo potencia
- El modelo es vendible, escalable y profesional

Este documento puede reutilizarse como base para otros rubros
(clínicas, academias, e-commerce, servicios profesionales).
