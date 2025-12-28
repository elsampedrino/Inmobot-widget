#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para estandarizar el JSON de demo al formato BBR
- Normaliza campos clave a minúsculas
- Adapta estructura a la estandarizada
- Mantiene compatibilidad con ambos workflows
"""

import json
from pathlib import Path
from datetime import datetime

# Rutas
JSON_DEMO = Path("Demo_Inmob/propiedades_demo.json")
JSON_OUTPUT = Path("Demo_Inmob/propiedades_demo.json")
BACKUP = Path(f"Demo_Inmob/propiedades_demo_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

def convertir_detalles_a_array(detalles_obj):
    """Convierte el objeto detalles al formato array usado en BBR"""
    detalles_array = []

    # Mapeo de campos booleanos
    if detalles_obj.get('cochera'):
        detalles_array.append('cochera')
    if detalles_obj.get('baulera'):
        detalles_array.append('baulera')
    if detalles_obj.get('balcon'):
        detalles_array.append('balcon')
    if detalles_obj.get('ascensor'):
        detalles_array.append('ascensor')

    # Campos adicionales comunes en demo
    if detalles_obj.get('mascotas'):
        detalles_array.append('acepta_mascotas')

    return detalles_array

def estandarizar_propiedad(prop):
    """Convierte una propiedad del formato demo al formato BBR estandarizado"""

    # 1. Normalizar tipo a minúsculas
    tipo_original = prop.get('tipo', 'Propiedad')
    tipo = tipo_original.lower()

    # 2. Normalizar operación a minúsculas
    operacion_original = prop.get('operacion', 'Venta')
    operacion = operacion_original.lower()

    # 3. Determinar estado de construcción basado en antigüedad
    antiguedad = prop.get('detalles', {}).get('antiguedad', 0)
    if antiguedad == 0:
        estado_construccion = 'a estrenar'
    else:
        estado_construccion = 'usado'

    # 4. Convertir detalles de objeto a array
    detalles_array = convertir_detalles_a_array(prop.get('detalles', {}))

    # 5. Ajustar expensas (en demo está fuera de precio)
    precio = prop.get('precio', {}).copy()
    if prop.get('expensas'):
        precio['expensas'] = prop['expensas']

    # 6. Ajustar características (baños vs banios)
    caracteristicas = prop.get('caracteristicas', {}).copy()
    if 'banios' in caracteristicas:
        caracteristicas['banios'] = caracteristicas.pop('banios')

    # Agregar superficie con formato string si viene como número
    if isinstance(caracteristicas.get('superficie_total'), (int, float)):
        caracteristicas['superficie_total'] = f"{caracteristicas['superficie_total']} m²"
    if isinstance(caracteristicas.get('superficie_cubierta'), (int, float)):
        caracteristicas['superficie_cubierta'] = f"{caracteristicas['superficie_cubierta']} m²"

    # 7. Construir propiedad estandarizada
    prop_estandarizada = {
        'id': prop['id'],
        'tipo': tipo,  # ✅ Minúsculas
        'operacion': operacion,  # ✅ Minúsculas
        'estado_construccion': estado_construccion,  # ✅ Minúsculas
        'titulo': prop['titulo'],
        'direccion': prop['direccion'],
        'precio': precio,
        'descripcion': prop.get('descripcion', ''),
        'fotos': {
            'carpeta': prop['fotos'].get('carpeta', ''),
            'urls': prop['fotos'].get('urls', [])
        },
        'caracteristicas': caracteristicas,
        'detalles': detalles_array  # ✅ Array como BBR
    }

    return prop_estandarizada

def main():
    print("=" * 70)
    print("ESTANDARIZACION DE JSON DEMO")
    print("=" * 70)
    print()

    # 1. Leer JSON demo
    print(f"1. Leyendo JSON demo: {JSON_DEMO}")
    with open(JSON_DEMO, 'r', encoding='utf-8') as f:
        data = json.load(f)

    propiedades = data.get('propiedades', [])
    print(f"   -> {len(propiedades)} propiedades")
    print()

    # 2. Crear backup
    print(f"2. Creando backup en: {BACKUP}")
    with open(BACKUP, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("   -> Backup creado")
    print()

    # 3. Estandarizar propiedades
    print("3. Estandarizando propiedades:")
    print()

    propiedades_estandarizadas = []

    for prop in propiedades:
        prop_id = prop['id']
        tipo_original = prop.get('tipo')
        operacion_original = prop.get('operacion')

        prop_nueva = estandarizar_propiedad(prop)

        print(f"  {prop_id}:")
        print(f"    tipo: '{tipo_original}' -> '{prop_nueva['tipo']}'")
        print(f"    operacion: '{operacion_original}' -> '{prop_nueva['operacion']}'")
        print(f"    estado_construccion: '{prop_nueva['estado_construccion']}'")
        print(f"    detalles: {prop_nueva['detalles']}")
        print()

        propiedades_estandarizadas.append(prop_nueva)

    # 4. Crear estructura final con metadata
    data_estandarizada = {
        'metadata': {
            'total_propiedades': len(propiedades_estandarizadas),
            'ultima_actualizacion': datetime.now().isoformat(),
            'version': '2.0.0',
            'formato': 'estandarizado_bbr',
            'descripcion': 'Catálogo de propiedades demo para testing',
            'notas': [
                {
                    'fecha': datetime.now().isoformat(),
                    'accion': 'Estandarización al formato BBR',
                    'cambios': [
                        'Normalización de tipo/operacion/estado_construccion a minúsculas',
                        'Conversión de detalles de objeto a array',
                        'Ajuste de expensas dentro de precio',
                        'Formato de superficie con unidades'
                    ]
                }
            ]
        },
        'propiedades': propiedades_estandarizadas
    }

    # 5. Guardar JSON estandarizado
    print("4. Guardando JSON estandarizado...")
    with open(JSON_OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(data_estandarizada, f, indent=2, ensure_ascii=False)
    print(f"   -> Guardado en: {JSON_OUTPUT}")
    print()

    # 6. Verificación
    print("5. Verificando estandarizacion...")
    valores_tipo = {p['tipo'] for p in propiedades_estandarizadas}
    valores_operacion = {p['operacion'] for p in propiedades_estandarizadas}
    valores_estado = {p['estado_construccion'] for p in propiedades_estandarizadas}

    print(f"   Tipos: {sorted(valores_tipo)}")
    print(f"   Operaciones: {sorted(valores_operacion)}")
    print(f"   Estados: {sorted(valores_estado)}")
    print()

    todos_minusculas = all(
        v.islower() for v in valores_tipo | valores_operacion | valores_estado
    )

    if todos_minusculas:
        print("   OK - Todos los valores en minusculas")
    else:
        print("   ADVERTENCIA: Algunos valores tienen mayusculas")
    print()

    print("=" * 70)
    print("ESTANDARIZACION COMPLETADA")
    print("=" * 70)
    print()
    print(f"Resumen:")
    print(f"  - Propiedades procesadas: {len(propiedades_estandarizadas)}")
    print(f"  - Backup guardado: {BACKUP.name}")
    print(f"  - Formato: BBR estandarizado")
    print(f"  - Normalizado: tipo, operacion, estado_construccion en minusculas")
    print(f"  - Detalles: convertidos a array")
    print()

if __name__ == "__main__":
    main()
