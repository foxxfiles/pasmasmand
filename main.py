#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestor de Contrasenas Seguras
Aplicacion para gestionar contrasenas con cifrado AES256
"""

import os
import sys
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk

# Agregar ruta del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.ui.login_window import LoginWindow
from src.utils.config import Config
from src.utils.pyinstaller_utils import ensure_vault_exists, is_pyinstaller

def check_dependencies():
    """Verifica que todas las dependencias esten instaladas"""
    try:
        import Crypto
        from Crypto.Cipher import AES
        return True
    except ImportError:
        messagebox.showerror(
            "Error de Dependencias",
            "No se encontraron todas las dependencias necesarias.\n"
            "Por favor, instale las dependencias con:\n"
            "pip install -r requirements.txt"
        )
        return False

def center_window(window, width, height):
    """Centra la ventana en la pantalla"""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    window.geometry(f"{width}x{height}+{x}+{y}")

def main():
    """Funcion principal que inicia la aplicacion"""
    # Verificar dependencias
    if not check_dependencies():
        return
    
    # Cargar configuracion
    config = Config()
    
    # Asegurar que el vault exista cuando se ejecuta desde PyInstaller
    if is_pyinstaller():
        print("DEBUG: Ejecutando desde PyInstaller, verificando vault...")
        ensure_vault_exists(config)
    
    # Crear ventana principal con tema oscuro
    root = ttk.Window(
        title="Gestor de Contrasenas Seguras",
        themename="darkly"
    )
    
    # Configurar tamano y posicion
    center_window(root, 800, 600)
    
    # Iniciar aplicacion
    app = LoginWindow(root, config)
    
    # Iniciar el bucle principal
    root.mainloop()

if __name__ == "__main__":
    main()