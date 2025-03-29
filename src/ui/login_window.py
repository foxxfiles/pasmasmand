#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ventana de inicio de sesion para el Gestor de Contrasenas
"""

import os
import tkinter as tk
from tkinter import messagebox, StringVar
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import traceback

from ..core.auth_manager import AuthManager
from ..storage.vault import PasswordVault
from .main_window import MainWindow

class LoginWindow:
    """Ventana de inicio de sesion"""
    
    def __init__(self, root, config):
        """Inicializa la ventana de login"""
        self.root = root
        self.config = config
        self.auth_manager = AuthManager()
        
        # Variables para las entradas
        self.master_key_var = StringVar()
        self.data_key_var = StringVar()
        self.new_vault_var = StringVar(value="0")
        
        # Contador de intentos fallidos
        self.failed_attempts = 0
        self.max_attempts = self.config.get("max_login_attempts", 5)
        
        # Configurar ventana
        self.setup_ui()
    
    def setup_ui(self):
        """Configura los elementos de la interfaz"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=BOTH, expand=YES)
        
        # Título
        title_label = ttk.Label(
            main_frame, 
            text="Gestor de Contraseñas Seguras",
            font=("TkDefaultFont", 16, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Frame para el formulario
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=X, expand=YES)
        
        # Campo para clave maestra
        ttk.Label(form_frame, text="Clave Maestra:").pack(fill=X, pady=(10, 0))
        master_entry = ttk.Entry(form_frame, textvariable=self.master_key_var, show="•")
        master_entry.pack(fill=X, pady=(5, 10))
        
        # Campo para clave de datos
        ttk.Label(form_frame, text="Clave de Datos:").pack(fill=X, pady=(10, 0))
        data_entry = ttk.Entry(form_frame, textvariable=self.data_key_var, show="•")
        data_entry.pack(fill=X, pady=(5, 10))
        
        # Opción para crear nuevo almacén
        create_frame = ttk.Frame(form_frame)
        create_frame.pack(fill=X, pady=10)
        
        create_check = ttk.Checkbutton(
            create_frame, 
            text="Crear nuevo almacén de contraseñas",
            variable=self.new_vault_var,
            onvalue="1",
            offvalue="0"
        )
        create_check.pack(side=LEFT)
        
        # Botones
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=X, pady=20)
        
        # Botón de acceso
        login_button = ttk.Button(
            buttons_frame,
            text="Acceder",
            command=self.authenticate,
            style="primary.TButton"
        )
        login_button.pack(side=RIGHT, padx=5)
        
        # Botón para salir
        exit_button = ttk.Button(
            buttons_frame,
            text="Salir",
            command=self.root.destroy
        )
        exit_button.pack(side=RIGHT, padx=5)
        
        # Poner el foco en el primer campo
        master_entry.focus_set()
        
        # Vincular evento Enter para autenticar
        self.root.bind("<Return>", lambda event: self.authenticate())
        
        # Información de seguridad
        info_text = (
            "La aplicación utiliza cifrado AES-256 para proteger sus contraseñas. "
            "Ambas claves son necesarias para acceder a sus datos."
        )
        info_label = ttk.Label(
            main_frame, 
            text=info_text,
            foreground="gray",
            justify=LEFT,
            wraplength=400
        )
        info_label.pack(pady=20, fill=X)
    
    def authenticate(self):
        """Verifica las credenciales e inicia sesion"""
        master_key = self.master_key_var.get()
        data_key = self.data_key_var.get()
        create_new = self.new_vault_var.get() == "1"
        
        # DEBUG: Mostrar las credenciales usadas (solo para depuración)
        print(f"DEBUG: Master key: {master_key}, Data key: {data_key}, Create new: {create_new}")
        
        # Validar que se hayan ingresado las claves
        if not master_key or not data_key:
            messagebox.showerror("Error", "Ambas claves son requeridas")
            return
        
        # Comprobar si existe el almacén
        vault = PasswordVault(self.auth_manager, self.config)
        vault_exists = vault.exists()
        
        # DEBUG: Comprobar si existe el almacén
        print(f"DEBUG: Vault exists: {vault_exists}, Path: {vault.vault_path}")
        
        if not vault_exists and not create_new:
            response = messagebox.askyesno(
                "Almacén no encontrado",
                "No se encontró un almacén de contraseñas. ¿Desea crear uno nuevo?"
            )
            if response:
                create_new = True
            else:
                return
        
        # Crear nuevo almacén o intentar abrir el existente
        if create_new and not vault_exists:
            # Configurar las claves en el administrador de autenticación
            self.auth_manager.set_keys(master_key, data_key)
            
            # Inicializar el almacén
            try:
                # DEBUG: Intentando crear nuevo almacén
                print("DEBUG: Intentando crear nuevo almacén")
                vault.initialize_vault()
                messagebox.showinfo(
                    "Éxito", 
                    "Se ha creado un nuevo almacén de contraseñas."
                )
                self.open_main_window()
            except Exception as e:
                # DEBUG: Error detallado
                print(f"DEBUG ERROR (crear): {str(e)}")
                print(traceback.format_exc())
                messagebox.showerror(
                    "Error", 
                    f"No se pudo crear el almacén: {str(e)}"
                )
        else:
            # Intentar autenticar con las claves proporcionadas
            try:
                # DEBUG: Intentando autenticar
                print("DEBUG: Intentando autenticar con claves existentes")
                self.auth_manager.set_keys(master_key, data_key)
                
                # DEBUG: Claves establecidas, probando test_keys
                test_result = vault.test_keys()
                print(f"DEBUG: Test keys result: {test_result}")
                
                if test_result:
                    # Autenticación exitosa
                    self.failed_attempts = 0
                    self.open_main_window()
                else:
                    # Autenticación fallida
                    self.failed_attempts += 1
                    remaining = self.max_attempts - self.failed_attempts
                    messagebox.showerror(
                        "Error de autenticación", 
                        f"Claves incorrectas. Intentos restantes: {remaining}"
                    )
                    
                    # Si se excedió el número máximo de intentos
                    if self.failed_attempts >= self.max_attempts:
                        messagebox.showerror(
                            "Acceso bloqueado", 
                            "Ha excedido el número máximo de intentos. La aplicación se cerrará."
                        )
                        self.root.destroy()
            except Exception as e:
                # DEBUG: Error detallado
                print(f"DEBUG ERROR (autenticar): {str(e)}")
                print(traceback.format_exc())
                messagebox.showerror(
                    "Error", 
                    f"Error al acceder al almacén: {str(e)}"
                )
    
    def open_main_window(self):
        """Abre la ventana principal después de autenticar"""
        # Ocultar la ventana de login
        self.root.withdraw()
        
        # Crear nueva ventana para la aplicación principal
        main_window = tk.Toplevel(self.root)
        main_window.title("Gestor de Contraseñas - Panel Principal")
        
        # Aplicar el mismo tema
        style = ttk.Style()
        
        # Configurar para que cuando se cierre la ventana principal, se cierre todo
        main_window.protocol("WM_DELETE_WINDOW", self.root.destroy)
        
        # Iniciar la aplicación principal
        app = MainWindow(main_window, self.auth_manager, self.config)
        
        # Centrar ventana
        window_width = 900
        window_height = 700
        screen_width = main_window.winfo_screenwidth()
        screen_height = main_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        main_window.geometry(f"{window_width}x{window_height}+{x}+{y}")