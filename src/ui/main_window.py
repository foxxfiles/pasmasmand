#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ventana principal del Gestor de Contrasenas
"""

import os
import time
import tkinter as tk
from tkinter import messagebox, StringVar, BooleanVar
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox

from .password_generator_dialog import PasswordGeneratorDialog
from .password_entry_dialog import PasswordEntryDialog
from ..core.password_manager import PasswordManager
from ..storage.vault import PasswordVault

class MainWindow:
    """Ventana principal de la aplicacion"""
    
    def __init__(self, root, auth_manager, config):
        """
        Inicializa la ventana principal
        
        Args:
            root: Ventana raíz de Tkinter
            auth_manager: Instancia de AuthManager
            config: Instancia de Config
        """
        self.root = root
        self.auth_manager = auth_manager
        self.config = config
        
        # Crear gestor de contraseñas
        self.vault = PasswordVault(auth_manager, config)
        self.password_manager = PasswordManager(self.vault)
        
        # Variables para la interfaz
        self.search_var = StringVar()
        self.status_var = StringVar(value="Listo")
        self.selected_id = None
        self.password_list = []
        self.sort_by = "service"  # Ordenar por servicio por defecto
        self.sort_ascending = True
        
        # Variable para control de inactividad
        self.auto_logout_time = self.config.get("auto_logout_minutes", 5) * 60 * 1000  # Convertir a milisegundos
        self.last_activity_time = time.time() * 1000
        
        # Configurar ventana
        self.setup_ui()
        
        # Cargar contraseñas
        self.load_passwords()
        
        # Iniciar temporizador de inactividad
        self.check_inactivity()
        
        # Configurar evento para detectar actividad
        self.root.bind("<Motion>", self.reset_inactivity_timer)
        self.root.bind("<Key>", self.reset_inactivity_timer)
    
    def setup_ui(self):
        """Configura los elementos de la interfaz"""
        # Establecer título
        self.root.title("Gestor de Contraseñas Seguras")
        
        # Crear menú principal
        self.create_menu()
        
        # Frame principal con 3 pixeles de padding
        main_frame = ttk.Frame(self.root, padding=3)
        main_frame.pack(fill=BOTH, expand=YES)
        
        # Frame para la barra de herramientas
        toolbar_frame = ttk.Frame(main_frame)
        toolbar_frame.pack(fill=X, pady=(0, 5))
        
        # Botones de la barra de herramientas
        ttk.Button(
            toolbar_frame,
            text="Nueva",
            command=self.add_password,
            bootstyle="success",
            width=10
        ).pack(side=LEFT, padx=2)
        
        ttk.Button(
            toolbar_frame,
            text="Editar",
            command=self.edit_password,
            bootstyle="primary",
            width=10
        ).pack(side=LEFT, padx=2)
        
        ttk.Button(
            toolbar_frame,
            text="Eliminar",
            command=self.delete_password,
            bootstyle="danger",
            width=10
        ).pack(side=LEFT, padx=2)
        
        ttk.Button(
            toolbar_frame,
            text="Generar",
            command=self.open_generator,
            bootstyle="info",
            width=10
        ).pack(side=LEFT, padx=2)
        
        # Barra de búsqueda
        search_frame = ttk.Frame(toolbar_frame)
        search_frame.pack(side=RIGHT, padx=2)
        
        ttk.Label(search_frame, text="Buscar:").pack(side=LEFT, padx=(5, 2))
        
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side=LEFT, padx=2)
        search_entry.bind("<KeyRelease>", self.search_passwords)
        
        ttk.Button(
            search_frame,
            text="X",
            command=self.clear_search,
            bootstyle="secondary",
            width=2
        ).pack(side=LEFT, padx=2)
        
        # Frame para la lista de contraseñas
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=BOTH, expand=YES)
        
        # Crear tabla para contraseñas (Treeview)
        columns = ("service", "username", "comment", "created_at")
        self.password_tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show="headings",
            bootstyle="primary"
        )
        
        # Configurar columnas
        self.password_tree.heading("service", text="Servicio", command=lambda: self.sort_treeview("service"))
        self.password_tree.heading("username", text="Usuario", command=lambda: self.sort_treeview("username"))
        self.password_tree.heading("comment", text="Comentario", command=lambda: self.sort_treeview("comment"))
        self.password_tree.heading("created_at", text="Creación", command=lambda: self.sort_treeview("created_at"))
        
        self.password_tree.column("service", width=150, anchor=W)
        self.password_tree.column("username", width=150, anchor=W)
        self.password_tree.column("comment", width=250, anchor=W)
        self.password_tree.column("created_at", width=100, anchor=W)
        
        # Barras de desplazamiento
        vscroll = ttk.Scrollbar(list_frame, orient=VERTICAL, command=self.password_tree.yview)
        self.password_tree.configure(yscrollcommand=vscroll.set)
        
        # Empaquetar elementos
        self.password_tree.pack(side=LEFT, fill=BOTH, expand=YES)
        vscroll.pack(side=RIGHT, fill=Y)
        
        # Asociar evento de selección
        self.password_tree.bind("<<TreeviewSelect>>", self.on_password_select)
        self.password_tree.bind("<Double-1>", self.view_password)
        
        # Frame para la barra de estado
        status_frame = ttk.Frame(main_frame, padding=(0, 5, 0, 0))
        status_frame.pack(fill=X, side=BOTTOM)
        
        # Barra de estado
        status_label = ttk.Label(status_frame, textvariable=self.status_var, anchor=W)
        status_label.pack(side=LEFT, fill=X, expand=YES)
        
        # Contador de contraseñas
        self.count_var = StringVar(value="0 contraseñas")
        count_label = ttk.Label(status_frame, textvariable=self.count_var, anchor=E)
        count_label.pack(side=RIGHT, padx=5)
    
    def create_menu(self):
        """Crea la barra de menú"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menú Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Nueva contraseña", command=self.add_password)
        file_menu.add_command(label="Generar contraseña", command=self.open_generator)
        file_menu.add_separator()
        file_menu.add_command(label="Cerrar sesión", command=self.logout)
        file_menu.add_command(label="Salir", command=self.root.destroy)
        
        # Menú Editar
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Editar", menu=edit_menu)
        edit_menu.add_command(label="Editar seleccionada", command=self.edit_password)
        edit_menu.add_command(label="Eliminar seleccionada", command=self.delete_password)
        edit_menu.add_separator()
        edit_menu.add_command(label="Copiar usuario", command=lambda: self.copy_field("username"))
        edit_menu.add_command(label="Copiar contraseña", command=lambda: self.copy_field("password"))
        
        # Menú Ayuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Acerca de", command=self.show_about)
    
    def load_passwords(self):
        """Carga las contraseñas del almacenamiento"""
        try:
            # Limpiar vista
            for item in self.password_tree.get_children():
                self.password_tree.delete(item)
            
            # Obtener contraseñas
            self.password_list = self.password_manager.get_all_passwords()
            
            # Ordenar según criterio actual
            self.sort_password_list()
            
            # Actualizar contador
            self.count_var.set(f"{len(self.password_list)} contraseñas")
            
            # Mostrar en la tabla
            for entry in self.password_list:
                values = (
                    entry.get("service", ""),
                    entry.get("username", ""),
                    entry.get("comment", ""),
                    entry.get("created_at", "").split("T")[0]  # Solo mostrar fecha
                )
                self.password_tree.insert("", END, iid=entry["id"], values=values)
            
            self.status_var.set("Contraseñas cargadas correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las contraseñas: {str(e)}")
            self.status_var.set("Error al cargar contraseñas")
    
    def sort_password_list(self):
        """Ordena la lista de contraseñas según el criterio actual"""
        # Función para obtener clave de ordenamiento
        def get_sort_key(entry):
            value = entry.get(self.sort_by, "")
            # Para fechas, asegurar formato ISO
            if self.sort_by in ["created_at", "updated_at"] and isinstance(value, str):
                return value
            # Para otros campos, convertir a minúsculas para ordenamiento no sensible a mayúsculas
            return str(value).lower()
        
        # Ordenar la lista
        self.password_list.sort(
            key=get_sort_key,
            reverse=not self.sort_ascending
        )
    
    def sort_treeview(self, column):
        """Ordena la tabla por columna"""
        if self.sort_by == column:
            # Si ya estaba ordenado por esta columna, invertir dirección
            self.sort_ascending = not self.sort_ascending
        else:
            # Nueva columna, ordenar ascendente
            self.sort_by = column
            self.sort_ascending = True
        
        # Recargar para aplicar ordenamiento
        self.load_passwords()
    
    def on_password_select(self, event):
        """Maneja el evento de selección en la tabla"""
        selected_items = self.password_tree.selection()
        if selected_items:
            self.selected_id = selected_items[0]
        else:
            self.selected_id = None
    
    def add_password(self):
        """Abre el diálogo para agregar contraseña"""
        dialog = PasswordEntryDialog(self.root, None, self)
        self.root.wait_window(dialog.dialog)
        
        # Si se guardó correctamente, recargar
        if dialog.result:
            self.load_passwords()
    
    def edit_password(self):
        """Edita la contraseña seleccionada"""
        if not self.selected_id:
            messagebox.showinfo("Información", "Por favor, seleccione una contraseña para editar")
            return
        
        try:
            # Obtener datos de la contraseña seleccionada
            entry = self.password_manager.get_password(self.selected_id)
            
            # Abrir diálogo de edición
            dialog = PasswordEntryDialog(self.root, entry, self)
            self.root.wait_window(dialog.dialog)
            
            # Si se guardó correctamente, recargar
            if dialog.result:
                self.load_passwords()
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo editar la contraseña: {str(e)}")
    
    def view_password(self, event=None):
        """Muestra los detalles de la contraseña seleccionada"""
        if not self.selected_id:
            messagebox.showinfo("Información", "Por favor, seleccione una contraseña para ver")
            return
        
        try:
            # Obtener datos de la contraseña seleccionada
            entry = self.password_manager.get_password(self.selected_id)
            
            # Mostrar diálogo de visualización (mismo que edición pero en modo solo lectura)
            dialog = PasswordEntryDialog(self.root, entry, self, readonly=True)
            self.root.wait_window(dialog.dialog)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo mostrar la contraseña: {str(e)}")
    
    def delete_password(self):
        """Elimina la contraseña seleccionada"""
        if not self.selected_id:
            messagebox.showinfo("Información", "Por favor, seleccione una contraseña para eliminar")
            return
        
        # Confirmar eliminación
        confirm = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Está seguro que desea eliminar esta contraseña? Esta acción no se puede deshacer."
        )
        
        if not confirm:
            return
        
        try:
            # Eliminar contraseña
            self.password_manager.delete_password(self.selected_id)
            
            # Recargar lista
            self.load_passwords()
            
            self.status_var.set("Contraseña eliminada correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar la contraseña: {str(e)}")
    
    def copy_field(self, field):
        """Copia un campo al portapapeles"""
        if not self.selected_id:
            messagebox.showinfo("Información", f"Por favor, seleccione una contraseña para copiar {field}")
            return
        
        try:
            # Obtener datos de la contraseña seleccionada
            entry = self.password_manager.get_password(self.selected_id)
            
            # Copiar al portapapeles
            value = entry.get(field, "")
            self.root.clipboard_clear()
            self.root.clipboard_append(value)
            
            self.status_var.set(f"{field.capitalize()} copiado al portapapeles")
            
            # Programar limpieza del portapapeles después de 30 segundos
            self.root.after(30000, self.clear_clipboard)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo copiar {field}: {str(e)}")
    
    def clear_clipboard(self):
        """Limpia el portapapeles por seguridad"""
        try:
            self.root.clipboard_clear()
            self.status_var.set("Portapapeles limpiado por seguridad")
        except:
            pass
    
    def search_passwords(self, event=None):
        """Busca contraseñas que coinciden con el criterio"""
        query = self.search_var.get().strip()
        
        if not query:
            # Si la búsqueda está vacía, mostrar todas
            self.load_passwords()
            return
        
        try:
            # Buscar contraseñas
            results = self.password_manager.search_passwords(query)
            
            # Limpiar vista
            for item in self.password_tree.get_children():
                self.password_tree.delete(item)
            
            # Mostrar resultados
            for entry in results:
                values = (
                    entry.get("service", ""),
                    entry.get("username", ""),
                    entry.get("comment", ""),
                    entry.get("created_at", "").split("T")[0]  # Solo mostrar fecha
                )
                self.password_tree.insert("", END, iid=entry["id"], values=values)
            
            # Actualizar contador
            self.count_var.set(f"{len(results)} contraseñas encontradas")
            
            self.status_var.set(f"Búsqueda completada: {len(results)} resultados")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en la búsqueda: {str(e)}")
    
    def clear_search(self):
        """Limpia la búsqueda y muestra todas las contraseñas"""
        self.search_var.set("")
        self.load_passwords()
    
    def open_generator(self):
        """Abre el generador de contraseñas"""
        dialog = PasswordGeneratorDialog(self.root)
        self.root.wait_window(dialog.dialog)
        
        # El generador solo genera, no modifica datos
    
    def show_about(self):
        """Muestra información sobre la aplicación"""
        about_text = """
        Gestor de Contraseñas Seguras
        Versión 1.0
        
        Una aplicación para gestionar contraseñas con cifrado AES256.
        
        Características:
        • Almacenamiento cifrado en dos niveles
        • Generador de contraseñas seguras
        • Sin persistencia de datos en texto plano
        
        Desarrollada con Python y Tkinter.
        """
        
        messagebox.showinfo("Acerca de", about_text)
    
    def logout(self):
        """Cierra la sesión actual"""
        # Limpiar datos en memoria
        self.auth_manager.clear_keys()
        
        # Cerrar ventana principal
        self.root.destroy()
    
    def reset_inactivity_timer(self, event=None):
        """Reinicia el temporizador de inactividad"""
        self.last_activity_time = time.time() * 1000
    
    def check_inactivity(self):
        """Verifica inactividad para cierre automático"""
        current_time = time.time() * 1000
        elapsed = current_time - self.last_activity_time
        
        if elapsed > self.auto_logout_time:
            # Cierre por inactividad
            messagebox.showinfo(
                "Cierre automático",
                "Se ha cerrado la sesión automáticamente por inactividad."
            )
            self.logout()
            return
        
        # Programar próxima verificación (cada 10 segundos)
        self.root.after(10000, self.check_inactivity)