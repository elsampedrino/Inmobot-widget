#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Optimizador Incremental de Fotos BBR
=====================================
Optimiza SOLO las carpetas nuevas que aún no han sido procesadas.

Uso:
    python optimizar_fotos_nuevas.py --carpeta-fotos ./fotos_sin_optimizar

Parámetros:
    --carpeta-fotos    : Carpeta con fotos originales (sin optimizar)
    --carpeta-salida   : Carpeta donde guardar optimizadas (default: fotos_numeradas)
    --max-width        : Ancho máximo en píxeles (default: 1920)
    --quality          : Calidad JPEG 0-100 (default: 85)
    --force            : Forzar re-optimización de todas las carpetas

Funcionamiento:
    1. Compara carpetas origen vs destino
    2. Optimiza SOLO las carpetas que faltan en destino
    3. Mantiene el mismo número de carpeta (1/ -> 1/, 2/ -> 2/, etc.)
    4. Redimensiona a max-width y comprime a quality%
    5. Elimina metadatos EXIF (privacidad)

Ejemplo:
    # Primera vez (optimiza todo)
    python optimizar_fotos_nuevas.py --carpeta-fotos ./fotos_originales

    # Actualizaciones (solo nuevas)
    python optimizar_fotos_nuevas.py --carpeta-fotos ./fotos_originales
    → Solo procesa carpetas que no existen en fotos_numeradas/
"""

import argparse
import sys
from pathlib import Path
from PIL import Image
import io

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ============================================
# CONFIGURACIÓN
# ============================================

VALID_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff'}

# ============================================
# FUNCIONES
# ============================================

def optimizar_imagen(input_path, output_path, max_width, quality):
    """
    Optimiza una imagen: redimensiona, comprime y elimina metadatos.

    Args:
        input_path: Path a imagen original
        output_path: Path donde guardar optimizada
        max_width: Ancho máximo en píxeles
        quality: Calidad JPEG (0-100)

    Returns:
        tuple: (success: bool, size_original: int, size_optimizada: int, error_msg: str)
    """
    try:
        # Tamaño original
        size_original = input_path.stat().st_size

        # Abrir imagen
        with Image.open(input_path) as img:
            # Convertir RGBA a RGB si es necesario
            if img.mode == 'RGBA':
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3])
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')

            # Redimensionar si es muy grande
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

            # Asegurar que la salida sea .jpg
            output_path = output_path.with_suffix('.jpg')

            # Guardar optimizada (sin metadatos EXIF)
            img.save(
                output_path,
                'JPEG',
                quality=quality,
                optimize=True,
                exif=b''  # Eliminar metadatos EXIF
            )

        # Tamaño optimizado
        size_optimizada = output_path.stat().st_size

        return True, size_original, size_optimizada, None

    except Exception as e:
        return False, 0, 0, str(e)


def obtener_carpetas_numeradas(base_path):
    """
    Obtiene lista de carpetas numeradas (1, 2, 3, etc.)

    Args:
        base_path: Path a carpeta base

    Returns:
        set: Conjunto de números de carpetas
    """
    if not base_path.exists():
        return set()

    carpetas = set()
    for item in base_path.iterdir():
        if item.is_dir() and item.name.isdigit():
            carpetas.add(int(item.name))

    return carpetas


def optimizar_carpeta(carpeta_num, input_base, output_base, max_width, quality):
    """
    Optimiza todas las fotos de una carpeta numerada.

    Args:
        carpeta_num: Número de carpeta (1, 2, 3, etc.)
        input_base: Path a carpeta de origen
        output_base: Path a carpeta de destino
        max_width: Ancho máximo
        quality: Calidad JPEG

    Returns:
        tuple: (exito: int, errores: int, bytes_ahorrados: int)
    """
    input_folder = input_base / str(carpeta_num)
    output_folder = output_base / str(carpeta_num)

    # Crear carpeta de salida
    output_folder.mkdir(parents=True, exist_ok=True)

    # Buscar imágenes
    imagenes = [f for f in input_folder.iterdir()
                if f.is_file() and f.suffix.lower() in VALID_EXTENSIONS]

    if not imagenes:
        print(f"  Carpeta {carpeta_num}/ vacia - SALTANDO")
        return 0, 0, 0

    print(f"\n  Carpeta {carpeta_num}/ - {len(imagenes)} fotos")

    exitos = 0
    errores = 0
    bytes_ahorrados = 0

    for img_file in sorted(imagenes):
        output_file = output_folder / img_file.name

        success, size_orig, size_opt, error = optimizar_imagen(
            img_file, output_file, max_width, quality
        )

        if success:
            ahorro = size_orig - size_opt
            reduccion = (ahorro / size_orig) * 100 if size_orig > 0 else 0

            print(f"    OK {img_file.name:12} -> {output_file.name:12} "
                  f"({size_orig//1024:4}KB -> {size_opt//1024:3}KB, "
                  f"-{reduccion:4.1f}%)")

            exitos += 1
            bytes_ahorrados += ahorro
        else:
            print(f"    ERROR {img_file.name}: {error}")
            errores += 1

    return exitos, errores, bytes_ahorrados


def main():
    """Función principal."""

    parser = argparse.ArgumentParser(
        description='Optimiza fotos nuevas de BBR (incremental)'
    )

    parser.add_argument(
        '--carpeta-fotos',
        required=True,
        help='Carpeta con fotos originales (sin optimizar)'
    )

    parser.add_argument(
        '--carpeta-salida',
        default='../BBR Grupo Inmobiliario/fotos_numeradas',
        help='Carpeta donde guardar optimizadas (default: fotos_numeradas)'
    )

    parser.add_argument(
        '--max-width',
        type=int,
        default=1920,
        help='Ancho maximo en pixeles (default: 1920)'
    )

    parser.add_argument(
        '--quality',
        type=int,
        default=85,
        help='Calidad JPEG 0-100 (default: 85)'
    )

    parser.add_argument(
        '--force',
        action='store_true',
        help='Forzar re-optimizacion de todas las carpetas'
    )

    args = parser.parse_args()

    # Validar paths
    input_base = Path(args.carpeta_fotos)
    output_base = Path(args.carpeta_salida)

    if not input_base.exists():
        print(f"ERROR: Carpeta de entrada no encontrada: {input_base}")
        sys.exit(1)

    # Obtener carpetas
    carpetas_origen = obtener_carpetas_numeradas(input_base)
    carpetas_destino = obtener_carpetas_numeradas(output_base)

    # Determinar qué carpetas procesar
    if args.force:
        carpetas_a_procesar = sorted(carpetas_origen)
        print("MODO FORCE: Re-optimizando TODAS las carpetas")
    else:
        carpetas_a_procesar = sorted(carpetas_origen - carpetas_destino)

    # Resumen inicial
    print("="*60)
    print("OPTIMIZADOR INCREMENTAL DE FOTOS BBR")
    print("="*60)
    print(f"Carpeta origen:  {input_base}")
    print(f"Carpeta destino: {output_base}")
    print(f"Configuracion:   {args.max_width}px max, calidad {args.quality}")
    print("-"*60)
    print(f"Carpetas en origen:  {len(carpetas_origen)}")
    print(f"Carpetas ya optim:   {len(carpetas_destino)}")
    print(f"Carpetas a procesar: {len(carpetas_a_procesar)}")

    if not carpetas_a_procesar:
        print("\nNo hay carpetas nuevas para procesar!")
        print("Use --force para re-optimizar todas")
        sys.exit(0)

    print(f"\nCarpetas: {carpetas_a_procesar}")
    print("="*60)

    # Crear carpeta destino si no existe
    output_base.mkdir(parents=True, exist_ok=True)

    # Procesar cada carpeta
    total_exitos = 0
    total_errores = 0
    total_bytes_ahorrados = 0

    for carpeta_num in carpetas_a_procesar:
        exitos, errores, bytes_ah = optimizar_carpeta(
            carpeta_num, input_base, output_base, args.max_width, args.quality
        )

        total_exitos += exitos
        total_errores += errores
        total_bytes_ahorrados += bytes_ah

    # Resumen final
    print("\n" + "="*60)
    print("RESUMEN")
    print("="*60)
    print(f"Carpetas procesadas: {len(carpetas_a_procesar)}")
    print(f"Fotos optimizadas:   {total_exitos}")
    print(f"Errores:             {total_errores}")
    print(f"Espacio ahorrado:    {total_bytes_ahorrados / 1024 / 1024:.2f} MB")

    if total_exitos > 0:
        promedio_ahorro = (total_bytes_ahorrados / total_exitos) / 1024
        print(f"Ahorro promedio:     {promedio_ahorro:.1f} KB por foto")

    print("\nProximo paso:")
    print("  python subir_fotos_cloudinary.py ... (subira solo fotos nuevas)")


if __name__ == '__main__':
    main()
