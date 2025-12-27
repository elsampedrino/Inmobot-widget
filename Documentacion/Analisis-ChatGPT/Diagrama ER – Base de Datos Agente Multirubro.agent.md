# Diagrama ER – Base de Datos Agente Comercial Inteligente Multirubro

```mermaid
erDiagram

    RUBROS {
        int id_rubro PK
        string nombre
        string descripcion
        boolean activo
    }

    EMPRESAS {
        int id_empresa PK
        string nombre
        int id_rubro FK
        int id_plan FK
        boolean permite_followup
        boolean activa
        datetime created_at
    }

    PLANES {
        int id_plan PK
        string nombre
        boolean followup_habilitado
        boolean ia_habilitada
        int max_leads_mes
    }

    PROPIEDADES {
        int id_propiedad PK
        int id_empresa FK
        string tipo
        string operacion
        string zona
        int ambientes
        decimal precio
        boolean mascotas
        string estado
    }

    LEADS {
        int id_lead PK
        int id_empresa FK
        string nombre
        string telefono
        string canal
        string estado
        datetime created_at
    }

    CONVERSACIONES {
        int id_conversacion PK
        int id_lead FK
        int id_empresa FK
        string canal
        datetime inicio
        datetime fin
    }

    MENSAJES {
        int id_mensaje PK
        int id_conversacion FK
        string emisor
        text mensaje
        datetime timestamp
    }

    FOLLOWUPS {
        int id_followup PK
        int id_lead FK
        int id_conversacion FK
        string tipo
        string estado
        datetime fecha_programada
        datetime fecha_ejecucion
    }

    CONTEXTOS_CONVERSACION {
        int id_contexto PK
        int id_conversacion FK
        text resumen_contexto
        datetime updated_at
    }

    RUBROS ||--o{ EMPRESAS : pertenece
    PLANES ||--o{ EMPRESAS : contrata
    EMPRESAS ||--o{ PROPIEDADES : publica
    EMPRESAS ||--o{ LEADS : recibe
    LEADS ||--o{ CONVERSACIONES : inicia
    CONVERSACIONES ||--o{ MENSAJES : contiene
    LEADS ||--o{ FOLLOWUPS : tiene
    CONVERSACIONES ||--o{ FOLLOWUPS : genera
    CONVERSACIONES ||--|| CONTEXTOS_CONVERSACION : mantiene
