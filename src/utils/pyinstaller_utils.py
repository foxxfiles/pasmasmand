#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilidades para manejar el entorno de PyInstaller
"""

import os
import sys
import shutil

def is_pyinstaller():
    """
    Determina si la aplicación está ejecutándose desde un ejecutable de PyInstaller
    
    Returns:
        bool: True si se está ejecutando desde un ejecutable PyInstaller
    """
    return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')

def get_application_path():
    """
    Obtiene la ruta base de la aplicación
    
    Returns:
        str: Ruta base de la aplicación
    """
    if is_pyinstaller():
        # Estamos en un ejecutable PyInstaller
        return os.path.dirname(sys.executable)
    else:
        # Estamos en un entorno de desarrollo
        return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def ensure_vault_exists(config):
    """
    Asegura que el archivo vault exista
    
    Args:
        config: Instancia de Config
        
    Returns:
        bool: True si el vault existe o se creó correctamente
    """
    vault_path = config.get_vault_path()
    
    # Verificar si el vault ya existe
    if os.path.exists(vault_path) and os.path.getsize(vault_path) > 0:
        print(f"DEBUG: Vault encontrado en {vault_path}")
        return True
    
    # El vault no existe, intentar crearlo
    try:
        # Asegurar que el directorio existe
        vault_dir = os.path.dirname(vault_path)
        os.makedirs(vault_dir, exist_ok=True)
        
        # Crear un archivo vacío
        with open(vault_path, 'wb') as f:
            f.write(b'')
        
        print(f"DEBUG: Vault vacío creado en {vault_path}")
        return True
    except Exception as e:
        print(f"DEBUG: Error al crear vault vacío: {str(e)}")
        return False