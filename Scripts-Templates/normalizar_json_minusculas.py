#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para normalizar campos clave del JSON a minúsculas
Esto mejora el matching con las consultas de usuarios que se normalizan en el prompt
"""

import json
from pathlib import Path
from datetime import datetime

# Rutas
RUTA_JSON = Path("BBR Grupo Inmobiliario/propiedades_bbr.json")
RUTA_BACKUP = Path(f"BBR Grupo Inmobiliario/propiedades_bbr_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

# Campos que deben normalizarse a minúsculas
CAMPOS_NORMALIZAR = [
    'tipo',           # Casa, Departamento, Local, Terreno -> casa, departamento, local, terreno
    'operacion',      # Venta, Alquiler -> venta, alquiler
    'estado_construccion'  # Usado, A estrenar -> usado, a estrenar
]

def normalizar_propiedad(prop):
    """Normaliza los campos clave de una propiedad a minúsculas"""
    prop_normalizada = prop.copy()

    for campo in CAMPOS_NORMALIZAR:
        if campo in prop_normalizada and prop_normalizada[campo]:
            valor_original = prop_normalizada[campo]
            valor_normalizado = valor_original.lower()

            if valor_original != valor_normalizado:
                print(f"  {prop['id']}: {campo} '{valor_original}' -> '{valor_normalizado}'")
                prop_normalizada[campo] = valor_normalizado

    return prop_normalizada

def main():
    print("=" * 70)
    print("NORMALIZACION DE JSON A MINUSCULAS")
    print("=" * 70)
    print()

    # 1. Leer JSON actual
    print(f"1. Leyendo JSON desde: {RUTA_JSON}")
    with open(RUTA_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)

    propiedades = data.get('propiedades', [])
    print(f"   -> {len(propiedades)} propiedades encontradas")
    print()

    # 2. Crear backup
    print(f"2. Creando backup en: {RUTA_BACKUP}")
    with open(RUTA_BACKUP, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("   -> Backup creado OK")
    print()

    # 3. Normalizar propiedades
    print("3. Normalizando campos a minusculas:")
    print()

    propiedades_normalizadas = []
    cambios_totales = 0

    for prop in propiedades:
        prop_normalizada = normalizar_propiedad(prop)
        propiedades_normalizadas.append(prop_normalizada)

        # Contar cambios
        for campo in CAMPOS_NORMALIZAR:
            if campo in prop and prop[campo] and prop[campo] != prop_normalizada.get(campo):
                cambios_totales += 1

    print()
    print(f"   -> Total de cambios: {cambios_totales}")
    print()

    # 4. Actualizar metadata
    data['propiedades'] = propiedades_normalizadas
    data['metadata']['ultima_actualizacion'] = datetime.now().isoformat()
    data['metadata']['version'] = data['metadata'].get('version', '1.0.0')

    # Agregar nota sobre normalización
    if 'notas' not in data['metadata']:
        data['metadata']['notas'] = []

    data['metadata']['notas'].append({
        'fecha': datetime.now().isoformat(),
        'accion': 'Normalización a minúsculas',
        'campos': CAMPOS_NORMALIZAR,
        'cambios': cambios_totales
    })

    # 5. Guardar JSON actualizado
    print("4. Guardando JSON normalizado...")
    with open(RUTA_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"   -> JSON actualizado: {RUTA_JSON}")
    print()

    # 6. Verificar normalización
    print("5. Verificando normalizacion...")
    valores_tipo = set()
    valores_operacion = set()
    valores_estado = set()

    for prop in propiedades_normalizadas:
        if 'tipo' in prop and prop['tipo']:
            valores_tipo.add(prop['tipo'])
        if 'operacion' in prop and prop['operacion']:
            valores_operacion.add(prop['operacion'])
        if 'estado_construccion' in prop and prop['estado_construccion']:
            valores_estado.add(prop['estado_construccion'])

    print(f"   Valores unicos en 'tipo': {sorted(valores_tipo)}")
    print(f"   Valores unicos en 'operacion': {sorted(valores_operacion)}")
    print(f"   Valores unicos en 'estado_construccion': {sorted(valores_estado)}")
    print()

    # Verificar que TODO esté en minúsculas
    errores = []
    for valor in list(valores_tipo) + list(valores_operacion) + list(valores_estado):
        if valor != valor.lower():
            errores.append(valor)

    if errores:
        print(f"   ADVERTENCIA: Valores que aun tienen mayusculas: {errores}")
    else:
        print("   OK - Todos los valores estan en minusculas")
    print()

    print("=" * 70)
    print("PROCESO COMPLETADO")
    print("=" * 70)
    print()
    print(f"Resumen:")
    print(f"  - Propiedades procesadas: {len(propiedades_normalizadas)}")
    print(f"  - Campos normalizados: {', '.join(CAMPOS_NORMALIZAR)}")
    print(f"  - Cambios realizados: {cambios_totales}")
    print(f"  - Backup guardado en: {RUTA_BACKUP.name}")
    print()
    print("Ahora el JSON esta 100% compatible con la normalizacion del prompt!")

if __name__ == "__main__":
    main()
