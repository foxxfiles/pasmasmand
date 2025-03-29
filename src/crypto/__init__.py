#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para crear los archivos __init__.py necesarios
"""

import os

# Directorios donde crear los __init__.py
directories = [
    "src",
    "src/ui",
    "src/core",
    "src/crypto",
    "src/storage",
    "src/utils"
]

# Contenido para cada __init__.py
contents = {
    "src": "# Paquete principal",
    "src/ui": "# Módulos de interfaz de usuario",
    "src/core": "# Módulos del núcleo de la aplicación",
    "src/crypto": "# Módulos de cifrado",
    "src/storage": "# Módulos de almacenamiento",
    "src/utils": "# Módulos de utilidades"
}

def create_init_files():
    """Crea los archivos __init__.py en cada directorio"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    for directory in directories:
        dir_path = os.path.join(base_dir, directory)
        init_path = os.path.join(dir_path, "__init__.py")
        
        # Asegurarse de que el directorio existe
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"Creado directorio: {dir_path}")
        
        # Crear __init__.py si no existe o está vacío
        if not os.path.exists(init_path) or os.path.getsize(init_path) == 0:
            with open(init_path, 'w', encoding='utf-8') as f:
                f.write(contents.get(directory, "# Módulo de la aplicación"))
            print(f"Creado archivo: {init_path}")
        else:
            print(f"El archivo ya existe: {init_path}")

if __name__ == "__main__":
    create_init_files()