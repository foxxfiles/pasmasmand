#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dialogo para crear o editar entradas de contrasenas
"""

import tkinter as tk
from tkinter import StringVar, BooleanVar, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from datetime import datetime

from .password_generator_dialog import PasswordGeneratorDialog

class PasswordEntryDialog:
    """Dialogo para crear o editar entradas de contrasenas"""
    
    def __init__(self, parent, entry=None, main_window=None, readonly=False):
        """
        Inicializa el dialogo de entrada/edicion
        
        Args:
            parent: Ventana padre
            entry: Entrada existente para edición (None para nueva)
            main_window: Referencia a la ventana principal
            readonly: Modo solo lectura para visualización
        """
        self.parent = parent
        self.entry = entry  # None para nueva entrada, objeto para edición
        self.main_window = main_window
        self.readonly = readonly
        self.result = None
        
        # Variables para los campos
        self.username_var = StringVar()
        self.service_var = StringVar()
        self.password_var = StringVar()
        self.comment_var = StringVar()
        self.show_password_var = BooleanVar(value=False)
        
        # Cargar datos de entrada existente
        if entry:
            self.username_var.set(entry.get("username", ""))
            self.service_var.set(entry.get("service", ""))
            self.password_var.set(entry.get("password", ""))
            self.comment_var.set(entry.get("comment", ""))
        
        # Crear ventana de dialogo
        self.dialog = tk.Toplevel(parent)
        
        # Título según modo
        if readonly:
            self.dialog.title("Ver Contraseña")
        elif entry:
            self.dialog.title("Editar Contraseña")
        else:
            self.dialog.title("Nueva Contraseña")
        
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.resizable(False, False)
        
        # Establecer posición centrada
        window_width = 500
        window_height = 400
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()
        x = int((screen_width - window_width) / 2)
        y = int((screen_height - window_height) / 2)
        self.dialog.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Configurar interfaz
        self.setup_ui()
    
    def setup_ui(self):
        """Configura los elementos de la interfaz"""
        # Contenedor principal
        main_frame = ttk.Frame(self.dialog, padding=15)
        main_frame.pack(fill=BOTH, expand=YES)
        
        # Título del formulario
        if self.readonly:
            title_text = "Detalles de la Contraseña"
            title_color = "info"
        elif self.entry:
            title_text = "Editar Contraseña"
            title_color = "primary"
        else:
            title_text = "Nueva Contraseña"
            title_color = "success"
        
        title_label = ttk.Label(
            main_frame,
            text=title_text,
            font=("TkDefaultFont", 14, "bold"),
            bootstyle=title_color
        )
        title_label.pack(pady=(0, 15), anchor=W)
        
        # Formulario de entrada
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=BOTH, expand=YES)
        
        # Campo: Servicio
        ttk.Label(form_frame, text="Servicio:").grid(row=0, column=0, sticky=W, pady=5)
        service_entry = ttk.Entry(
            form_frame,
            textvariable=self.service_var,
            width=40,
            state="readonly" if self.readonly else "normal"
        )
        service_entry.grid(row=0, column=1, sticky=(W, E), padx=5, pady=5)
        
        # Campo: Usuario
        ttk.Label(form_frame, text="Usuario:").grid(row=1, column=0, sticky=W, pady=5)
        username_entry = ttk.Entry(
            form_frame,
            textvariable=self.username_var,
            width=40,
            state="readonly" if self.readonly else "normal"
        )
        username_entry.grid(row=1, column=1, sticky=(W, E), padx=5, pady=5)
        
        # Campo: Contraseña
        ttk.Label(form_frame, text="Contraseña:").grid(row=2, column=0, sticky=W, pady=5)
        
        # Frame para contraseña y botones
        password_frame = ttk.Frame(form_frame)
        password_frame.grid(row=2, column=1, sticky=(W, E), padx=5, pady=5)
        
        # Campo de contraseña
        self.password_entry = ttk.Entry(  # Guardar referencia al Entry de contraseña
            password_frame,
            textvariable=self.password_var,
            width=30,
            show="•",
            state="readonly" if self.readonly else "normal"
        )
        self.password_entry.pack(side=LEFT, fill=X, expand=YES)
        
        # Botón para mostrar/ocultar
        show_button = ttk.Button(
            password_frame,
            text="👁️",
            command=self.show_hide_password,
            width=3,
            bootstyle="secondary-outline"
        )
        show_button.pack(side=LEFT, padx=2)
        
        # Botón para generar
        if not self.readonly:
            generate_button = ttk.Button(
                password_frame,
                text="🎲",
                command=self.open_generator,
                width=3,
                bootstyle="info-outline"
            )
            generate_button.pack(side=LEFT, padx=2)
        
        # Casilla para mostrar/ocultar
        show_check = ttk.Checkbutton(
            form_frame,
            text="Mostrar contraseña",
            variable=self.show_password_var,
            command=self.update_password_display,
            bootstyle="info-round-toggle"
        )
        show_check.grid(row=3, column=1, sticky=W, padx=5, pady=5)
        
        # Campo: Comentario
        ttk.Label(form_frame, text="Comentario:").grid(row=4, column=0, sticky=W, pady=5)
        comment_text = tk.Text(
            form_frame,
            height=5,
            width=40,
            wrap=tk.WORD,
            font=("TkDefaultFont", 10)
        )
        comment_text.grid(row=4, column=1, sticky=(W, E), padx=5, pady=5)
        
        # Insertar texto existente
        comment_text.insert("1.0", self.comment_var.get())
        
        # Configurar como solo lectura si es necesario
        if self.readonly:
            comment_text.config(state="disabled")
        
        # Enlazar texto para actualizar variable
        def update_comment(*args):
            self.comment_var.set(comment_text.get("1.0", "end-1c"))
        
        comment_text.bind("<KeyRelease>", update_comment)
        
        # Información de fecha para entradas existentes
        if self.entry and (self.entry.get("created_at") or self.entry.get("updated_at")):
            info_frame = ttk.Frame(main_frame)
            info_frame.pack(fill=X, pady=(15, 0))
            
            # Fecha de creación
            if self.entry.get("created_at"):
                created_date = self.entry["created_at"].split("T")[0]
                ttk.Label(
                    info_frame,
                    text=f"Creado: {created_date}",
                    bootstyle="secondary"
                ).pack(side=LEFT)
            
            # Fecha de actualización
            if self.entry.get("updated_at") and self.entry.get("updated_at") != self.entry.get("created_at"):
                updated_date = self.entry["updated_at"].split("T")[0]
                ttk.Label(
                    info_frame,
                    text=f"Actualizado: {updated_date}",
                    bootstyle="secondary"
                ).pack(side=RIGHT)
        
        # Botones de acción
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=X, pady=(15, 0))
        
        if self.readonly:
            # Solo botón de cerrar en modo lectura
            ttk.Button(
                buttons_frame,
                text="Cerrar",
                command=self.dialog.destroy,
                width=10
            ).pack(side=RIGHT, padx=5)
            
            # Botón para generar QR
            ttk.Button(
                buttons_frame,
                text="Generar QR",
                command=self.generate_qr,
                style="info.TButton",
                width=10
            ).pack(side=RIGHT, padx=5)
            
            # Botones para copiar
            ttk.Button(
                buttons_frame,
                text="Copiar Usuario",
                command=lambda: self.copy_to_clipboard(self.username_var.get()),
                width=15,
                bootstyle="info"
            ).pack(side=LEFT, padx=5)
            
            ttk.Button(
                buttons_frame,
                text="Copiar Contraseña",
                command=lambda: self.copy_to_clipboard(self.password_var.get()),
                width=15,
                bootstyle="info"
            ).pack(side=LEFT, padx=5)
        else:
            # Botones de guardar y cancelar
            ttk.Button(
                buttons_frame,
                text="Cancelar",
                command=self.dialog.destroy,
                width=10
            ).pack(side=RIGHT, padx=5)
            
            ttk.Button(
                buttons_frame,
                text="Guardar",
                command=self.save,
                width=10,
                bootstyle="success"
            ).pack(side=RIGHT, padx=5)
        
        # Ajustar tabulación
        service_entry.focus_set()
    
    def show_hide_password(self):
        """Muestra u oculta la contraseña"""
        current_state = self.show_password_var.get()
        self.show_password_var.set(not current_state)
        self.update_password_display()
    
    def update_password_display(self):
        """Actualiza la visualización de la contraseña según el estado del checkbox"""
        # Método simplificado para evitar el error
        show_char = "" if self.show_password_var.get() else "•"
        self.password_entry.config(show=show_char)
    
    def open_generator(self):
        """Abre el generador de contraseñas"""
        dialog = PasswordGeneratorDialog(self.dialog)
        self.dialog.wait_window(dialog.dialog)
        
        # Si se generó una contraseña, usarla
        if dialog.password_var.get():
            self.password_var.set(dialog.password_var.get())
    
    def copy_to_clipboard(self, text):
        """Copia texto al portapapeles"""
        if text:
            self.dialog.clipboard_clear()
            self.dialog.clipboard_append(text)
            
            # Notificar en el título temporalmente
            original_title = self.dialog.title()
            self.dialog.title("¡Copiado al portapapeles!")
            self.dialog.after(1500, lambda: self.dialog.title(original_title))
            
    def generate_qr(self):
        """Genera un código QR con la información de la contraseña"""
        try:
            import qrcode
            from io import BytesIO
            from tkinter import Toplevel, Label
            
            # Crear datos para el QR
            qr_data = f"Servicio: {self.service_var.get()}\nUsuario: {self.username_var.get()}\nContraseña: {self.password_var.get()}"
            
            # Generar QR
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(qr_data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Mostrar en una nueva ventana
            qr_window = Toplevel(self.dialog)
            qr_window.title("Código QR de la Contraseña")
            
            # Convertir imagen a formato compatible con Tkinter
            bio = BytesIO()
            img.save(bio, format="PNG")
            img_bytes = bio.getvalue()
            
            # Mostrar imagen
            photo = tk.PhotoImage(data=img_bytes)
            label = Label(qr_window, image=photo)
            label.image = photo  # Mantener referencia
            label.pack(padx=10, pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el código QR: {str(e)}")
    
    def save(self):
        """Guarda los datos y cierra el diálogo"""
        # Validar campos obligatorios
        service = self.service_var.get().strip()
        username = self.username_var.get().strip()
        password = self.password_var.get()
        
        if not service:
            messagebox.showerror("Error", "El campo 'Servicio' es obligatorio")
            return
        
        if not username:
            messagebox.showerror("Error", "El campo 'Usuario' es obligatorio")
            return
        
        if not password:
            messagebox.showerror("Error", "El campo 'Contraseña' es obligatorio")
            return
        
        # Crear diccionario con datos
        entry_data = {
            "service": service,
            "username": username,
            "password": password,
            "comment": self.comment_var.get()
        }
        
        try:
            # Si es una entrada existente, actualizar
            if self.entry:
                self.main_window.password_manager.update_password(self.entry["id"], entry_data)
                self.main_window.status_var.set(f"Contraseña para {service} actualizada")
            else:
                # Si es nueva, agregar
                new_id = self.main_window.password_manager.add_password(entry_data)
                self.main_window.status_var.set(f"Nueva contraseña para {service} creada")
            
            # Indicar éxito
            self.result = True
            
            # Cerrar diálogo
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la contraseña: {str(e)}")