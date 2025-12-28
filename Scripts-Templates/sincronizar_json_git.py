#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para sincronizar el JSON normalizado al repositorio bot-inmobiliaria-data
Usa git clone/commit/push directamente (más simple que la API)
"""

import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
import tempfile

# Configuración
REPO_URL = "https://github.com/elsampedrino/bot-inmobiliaria-data.git"
FILE_TO_SYNC = "propiedades_bbr.json"
JSON_LOCAL = Path("BBR Grupo Inmobiliario/propiedades_bbr.json")

def run_git_command(cmd, cwd):
    """Ejecuta un comando git y retorna el resultado"""
    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        shell=True
    )
    return result.returncode, result.stdout, result.stderr

def main():
    print("=" * 70)
    print("SINCRONIZACION DE JSON A bot-inmobiliaria-data")
    print("=" * 70)
    print()

    # 1. Leer JSON local
    print(f"1. Leyendo JSON local: {JSON_LOCAL}")
    if not JSON_LOCAL.exists():
        print(f"   ERROR: No se encuentra el archivo {JSON_LOCAL}")
        return

    with open(JSON_LOCAL, 'r', encoding='utf-8') as f:
        data = json.load(f)

    propiedades = data.get('propiedades', [])
    print(f"   -> {len(propiedades)} propiedades")
    print(f"   -> Ultima actualizacion: {data['metadata']['ultima_actualizacion']}")
    print()

    # 2. Verificar normalización
    print("2. Verificando normalizacion...")
    valores_tipo = {p.get('tipo') for p in propiedades if p.get('tipo')}
    valores_operacion = {p.get('operacion') for p in propiedades if p.get('operacion')}

    print(f"   -> Tipos: {sorted(valores_tipo)}")
    print(f"   -> Operaciones: {sorted(valores_operacion)}")

    todos_minusculas = all(v.islower() for v in valores_tipo | valores_operacion)
    if todos_minusculas:
        print("   OK - Todo en minusculas")
    else:
        print("   ADVERTENCIA: Algunos valores tienen mayusculas")
    print()

    # 3. Crear directorio temporal
    print("3. Creando directorio temporal...")
    temp_dir = Path(tempfile.mkdtemp(prefix="bot-inmobiliaria-"))
    print(f"   -> {temp_dir}")
    print()

    try:
        # 4. Clonar repositorio
        print(f"4. Clonando repositorio {REPO_URL}...")
        code, stdout, stderr = run_git_command(f'git clone {REPO_URL} .', temp_dir)

        if code != 0:
            print(f"   ERROR al clonar: {stderr}")
            return

        print("   OK - Repositorio clonado")
        print()

        # 5. Copiar JSON actualizado
        print(f"5. Copiando {FILE_TO_SYNC}...")
        dest_file = temp_dir / FILE_TO_SYNC
        shutil.copy2(JSON_LOCAL, dest_file)
        print(f"   -> {dest_file}")
        print()

        # 6. Verificar cambios
        print("6. Verificando cambios con git diff...")
        code, stdout, stderr = run_git_command('git diff --stat', temp_dir)

        if stdout.strip():
            print(f"   Cambios detectados:")
            print(f"   {stdout}")
        else:
            print("   -> No hay cambios (JSON ya esta actualizado)")
            return
        print()

        # 7. Agregar cambios
        print("7. Agregando cambios al stage...")
        code, stdout, stderr = run_git_command(f'git add {FILE_TO_SYNC}', temp_dir)

        if code != 0:
            print(f"   ERROR: {stderr}")
            return

        print("   OK")
        print()

        # 8. Crear commit
        print("8. Creando commit...")
        commit_msg = f"""Actualizar catalogo BBR con normalizacion a minusculas

- Normalizar tipo, operacion, estado_construccion a minusculas
- Total: {len(propiedades)} propiedades
- Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Mejora el matching con consultas normalizadas en el prompt.
"""

        # Escapar comillas en el mensaje
        commit_msg_escaped = commit_msg.replace('"', '\\"').replace('\n', '\\n')

        code, stdout, stderr = run_git_command(
            f'git commit -m "{commit_msg_escaped}"',
            temp_dir
        )

        if code != 0:
            print(f"   ERROR al crear commit: {stderr}")
            return

        print("   OK - Commit creado")
        print()

        # 9. Push a GitHub
        print("9. Subiendo cambios a GitHub (git push)...")
        code, stdout, stderr = run_git_command('git push origin main', temp_dir)

        if code != 0:
            print(f"   ERROR al hacer push: {stderr}")
            print()
            print("   Posibles causas:")
            print("   - No tienes permisos de escritura en el repo")
            print("   - Necesitas autenticacion (token de GitHub)")
            print()
            print("   Solucion manual:")
            print(f"   1. cd {temp_dir}")
            print("   2. git push origin main")
            return

        print("   OK - Cambios subidos a GitHub")
        print()

    finally:
        # 10. Limpiar directorio temporal
        print("10. Limpiando directorio temporal...")
        shutil.rmtree(temp_dir, ignore_errors=True)
        print("    OK")
        print()

    print("=" * 70)
    print("SINCRONIZACION COMPLETADA")
    print("=" * 70)
    print()
    print(f"El JSON normalizado se subio correctamente a:")
    print(f"  https://github.com/elsampedrino/bot-inmobiliaria-data")
    print()
    print(f"URL Raw (usada por N8N):")
    print(f"  https://raw.githubusercontent.com/elsampedrino/bot-inmobiliaria-data/main/{FILE_TO_SYNC}")
    print()
    print("IMPORTANTE: GitHub Raw puede tardar 1-2 minutos en actualizar el cache")
    print()

if __name__ == "__main__":
    main()
