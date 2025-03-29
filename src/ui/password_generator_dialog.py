#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dialogo para generar contrasenas seguras
"""

import tkinter as tk
from tkinter import StringVar, IntVar, BooleanVar
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from ..core.password_generator import PasswordGenerator

class PasswordGeneratorDialog:
    """Dialogo para generar contrasenas seguras"""
    
    def __init__(self, parent):
        """
        Inicializa el diálogo de generación de contraseñas
        
        Args:
            parent: Ventana padre
        """
        self.parent = parent
        self.generator = PasswordGenerator()
        
        # Variables para los campos
        self.password_var = StringVar()
        self.length_var = IntVar(value=16)
        self.use_lowercase_var = BooleanVar(value=True)
        self.use_uppercase_var = BooleanVar(value=True)
        self.use_digits_var = BooleanVar(value=True)
        self.use_special_var = BooleanVar(value=True)
        self.exclude_similar_var = BooleanVar(value=False)
        self.exclude_ambiguous_var = BooleanVar(value=False)
        self.entropy_var = StringVar(value="")
        
        # Crear ventana de dialogo
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Generador de Contraseñas")
        self.dialog.transient(parent)
        self.dialog.resizable(False, False)
        
        # Establecer posición centrada
        window_width = 450
        window_height = 450
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()
        x = int((screen_width - window_width) / 2)
        y = int((screen_height - window_height) / 2)
        self.dialog.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Configurar interfaz
        self.setup_ui()
        
        # Generar contraseña inicial
        self.generate_password()
    
    def setup_ui(self):
        """Configura los elementos de la interfaz"""
        # Contenedor principal
        main_frame = ttk.Frame(self.dialog, padding=15)
        main_frame.pack(fill=BOTH, expand=YES)
        
        # Título
        title_label = ttk.Label(
            main_frame,
            text="Generador de Contraseñas Seguras",
            font=("TkDefaultFont", 14, "bold"),
            bootstyle="info"
        )
        title_label.pack(pady=(0, 15), anchor=W)
        
        # Campo de contraseña generada
        ttk.Label(main_frame, text="Contraseña generada:").pack(anchor=W, pady=(0, 5))
        
        password_frame = ttk.Frame(main_frame)
        password_frame.pack(fill=X, pady=(0, 15))
        
        password_entry = ttk.Entry(
            password_frame,
            textvariable=self.password_var,
            width=40,
            font=("Consolas", 10)
        )
        password_entry.pack(side=LEFT, fill=X, expand=YES)
        
        # Botones para acciones rápidas
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=X, pady=(0, 15))
        
        ttk.Button(
            action_frame,
            text="Generar",
            command=self.generate_password,
            bootstyle="success",
            width=10
        ).pack(side=LEFT, padx=5)
        
        ttk.Button(
            action_frame,
            text="Copiar",
            command=self.copy_to_clipboard,
            bootstyle="info",
            width=10
        ).pack(side=LEFT, padx=5)
        
        # Opciones de generación
        options_frame = ttk.LabelFrame(main_frame, text="Opciones de generación", padding=10)
        options_frame.pack(fill=X)
        
        # Longitud
        length_frame = ttk.Frame(options_frame)
        length_frame.pack(fill=X, pady=5)
        
        ttk.Label(length_frame, text="Longitud:").pack(side=LEFT, padx=(0, 10))
        
        length_slider = ttk.Scale(
            length_frame,
            from_=4,
            to=64,
            variable=self.length_var,
            command=self.on_length_change,
            bootstyle="info"
        )
        length_slider.pack(side=LEFT, fill=X, expand=YES)
        
        length_label = ttk.Label(length_frame, textvariable=self.length_var, width=3)
        length_label.pack(side=LEFT, padx=5)
        
        # Conjunto de caracteres
        chars_frame = ttk.Frame(options_frame)
        chars_frame.pack(fill=X, pady=5)
        
        # Columna 1
        col1 = ttk.Frame(chars_frame)
        col1.pack(side=LEFT, fill=Y, expand=YES)
        
        ttk.Checkbutton(
            col1,
            text="Minúsculas (a-z)",
            variable=self.use_lowercase_var,
            command=self.on_option_change,
            bootstyle="info-round-toggle"
        ).pack(anchor=W, pady=2)
        
        ttk.Checkbutton(
            col1,
            text="Mayúsculas (A-Z)",
            variable=self.use_uppercase_var,
            command=self.on_option_change,
            bootstyle="info-round-toggle"
        ).pack(anchor=W, pady=2)
        
        # Columna 2
        col2 = ttk.Frame(chars_frame)
        col2.pack(side=LEFT, fill=Y, expand=YES)
        
        ttk.Checkbutton(
            col2,
            text="Números (0-9)",
            variable=self.use_digits_var,
            command=self.on_option_change,
            bootstyle="info-round-toggle"
        ).pack(anchor=W, pady=2)
        
        ttk.Checkbutton(
            col2,
            text="Símbolos (!@#$%)",
            variable=self.use_special_var,
            command=self.on_option_change,
            bootstyle="info-round-toggle"
        ).pack(anchor=W, pady=2)
        
        # Exclusiones
        exclude_frame = ttk.Frame(options_frame)
        exclude_frame.pack(fill=X, pady=5)
        
        ttk.Checkbutton(
            exclude_frame,
            text="Excluir caracteres similares (i, l, 1, L, o, 0, O)",
            variable=self.exclude_similar_var,
            command=self.on_option_change,
            bootstyle="info-round-toggle"
        ).pack(anchor=W, pady=2)
        
        ttk.Checkbutton(
            exclude_frame,
            text="Excluir caracteres ambiguos (` ' \" \\)",
            variable=self.exclude_ambiguous_var,
            command=self.on_option_change,
            bootstyle="info-round-toggle"
        ).pack(anchor=W, pady=2)
        
        # Tipos adicionales de contraseñas
        types_frame = ttk.LabelFrame(main_frame, text="Tipos de contraseñas", padding=10)
        types_frame.pack(fill=X, pady=15)
        
        ttk.Button(
            types_frame,
            text="Memorable",
            command=self.generate_memorable,
            bootstyle="secondary-outline",
            width=15
        ).pack(side=LEFT, padx=5)
        
        ttk.Button(
            types_frame,
            text="PIN (6 dígitos)",
            command=self.generate_pin,
            bootstyle="secondary-outline", 
            width=15
        ).pack(side=LEFT, padx=5)
        
        ttk.Button(
            types_frame,
            text="Solo letras",
            command=self.generate_letters_only,
            bootstyle="secondary-outline",
            width=15
        ).pack(side=LEFT, padx=5)
        
        # Información de fortaleza
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=X, pady=(15, 0))
        
        ttk.Label(
            info_frame,
            text="Fortaleza:",
        ).pack(side=LEFT)
        
        ttk.Label(
            info_frame,
            textvariable=self.entropy_var,
            bootstyle="info"
        ).pack(side=LEFT, padx=5)
        
        # Botones de acción
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=X, pady=(15, 0))
        
        ttk.Button(
            buttons_frame,
            text="Usar",
            command=self.use_password,
            bootstyle="success",
            width=10
        ).pack(side=LEFT, padx=5)
        
        ttk.Button(
            buttons_frame,
            text="Cerrar",
            command=self.dialog.destroy,
            width=10
        ).pack(side=RIGHT, padx=5)
    
    def on_length_change(self, event=None):
        """Maneja el cambio en el deslizador de longitud"""
        self.generate_password()
    
    def on_option_change(self):
        """Maneja el cambio en las opciones de generación"""
        # Asegurarse que al menos una opción de caracteres esté activa
        if not any([
            self.use_lowercase_var.get(),
            self.use_uppercase_var.get(),
            self.use_digits_var.get(),
            self.use_special_var.get()
        ]):
            # Si todas están desactivadas, activar minúsculas
            self.use_lowercase_var.set(True)
        
        self.generate_password()
    
    def generate_password(self):
        """Genera una nueva contraseña con las opciones seleccionadas"""
        try:
            # Configurar generador
            self.generator.configure(
                length=self.length_var.get(),
                use_lowercase=self.use_lowercase_var.get(),
                use_uppercase=self.use_uppercase_var.get(),
                use_digits=self.use_digits_var.get(),
                use_special=self.use_special_var.get(),
                exclude_similar=self.exclude_similar_var.get(),
                exclude_ambiguous=self.exclude_ambiguous_var.get()
            )
            
            # Generar contraseña
            password = self.generator.generate()
            self.password_var.set(password)
            
            # Calcular y mostrar entropía
            entropy = self.generator.get_entropy(password)
            strength = self.generator.get_strength_description(entropy)
            self.entropy_var.set(f"{strength} (Entropía: {entropy:.1f} bits)")
            
        except Exception as e:
            self.password_var.set("")
            self.entropy_var.set(f"Error: {str(e)}")
    
    def generate_memorable(self):
        """Genera una contraseña memorable"""
        try:
            password = self.generator.generate_memorable(num_words=4)
            self.password_var.set(password)
            
            # Calcular y mostrar entropía
            entropy = self.generator.get_entropy(password)
            strength = self.generator.get_strength_description(entropy)
            self.entropy_var.set(f"{strength} (Entropía: {entropy:.1f} bits)")
            
        except Exception as e:
            self.password_var.set("")
            self.entropy_var.set(f"Error: {str(e)}")
    
    def generate_pin(self):
        """Genera un PIN numérico de 6 dígitos"""
        try:
            # Configurar para generar solo dígitos
            self.generator.configure(
                length=6,
                use_lowercase=False,
                use_uppercase=False,
                use_digits=True,
                use_special=False
            )
            
            # Actualizar UI para reflejar configuración
            self.length_var.set(6)
            self.use_lowercase_var.set(False)
            self.use_uppercase_var.set(False)
            self.use_digits_var.set(True)
            self.use_special_var.set(False)
            
            # Generar PIN
            pin = self.generator.generate()
            self.password_var.set(pin)
            
            # Calcular entropía (baja para PINs)
            entropy = self.generator.get_entropy(pin)
            strength = self.generator.get_strength_description(entropy)
            self.entropy_var.set(f"{strength} (Entropía: {entropy:.1f} bits)")
            
        except Exception as e:
            self.password_var.set("")
            self.entropy_var.set(f"Error: {str(e)}")
    
    def generate_letters_only(self):
        """Genera una contraseña solo con letras"""
        try:
            # Configurar para generar solo letras
            self.generator.configure(
                length=self.length_var.get(),
                use_lowercase=True,
                use_uppercase=True,
                use_digits=False,
                use_special=False
            )
            
            # Actualizar UI para reflejar configuración
            self.use_lowercase_var.set(True)
            self.use_uppercase_var.set(True)
            self.use_digits_var.set(False)
            self.use_special_var.set(False)
            
            # Generar contraseña
            password = self.generator.generate()
            self.password_var.set(password)
            
            # Calcular entropía
            entropy = self.generator.get_entropy(password)
            strength = self.generator.get_strength_description(entropy)
            self.entropy_var.set(f"{strength} (Entropía: {entropy:.1f} bits)")
            
        except Exception as e:
            self.password_var.set("")
            self.entropy_var.set(f"Error: {str(e)}")
    
    def copy_to_clipboard(self):
        """Copia la contraseña al portapapeles"""
        password = self.password_var.get()
        if password:
            self.dialog.clipboard_clear()
            self.dialog.clipboard_append(password)
            
            # Cambiar temporalmente el título para indicar que se copió
            original_title = self.dialog.title()
            self.dialog.title("¡Copiado al portapapeles!")
            self.dialog.after(1500, lambda: self.dialog.title(original_title))
    
    def use_password(self):
        """Usa la contraseña generada y cierra el diálogo"""
        # La contraseña queda en self.password_var para que la ventana que
        # llamó al diálogo pueda acceder a ella
        self.dialog.destroy()