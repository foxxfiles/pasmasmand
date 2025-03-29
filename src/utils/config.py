#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuracion de la aplicacion
"""

import os
import json
import datetime

# Configuracion predeterminada
DEFAULT_CONFIG = {
    "theme": "darkly",
    "auto_logout_minutes": 5,
    "vault_path": "passwords_new.vault",  # CAMBIADO: Nombre de archivo diferente
    "recent_services": [],
    "last_access": None,
    "max_login_attempts": 5,
    "min_password_length": 8
}

class Config:
    """Gestiona la configuracion de la aplicacion"""
    
    def __init__(self, config_file=None):
        """Inicializa la configuracion"""
        self.config_file = config_file or os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "config.json"
        )
        self.config = self.load()
        
    def load(self):
        """Carga la configuracion desde archivo"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # Forzar el uso del nuevo nombre de almacén
                    config["vault_path"] = DEFAULT_CONFIG["vault_path"]
                    # Asegurarse que todos los valores predeterminados existan
                    for key, value in DEFAULT_CONFIG.items():
                        if key not in config:
                            config[key] = value
                    return config
            except Exception as e:
                print(f"Error al cargar configuracion: {e}")
                return DEFAULT_CONFIG.copy()
        return DEFAULT_CONFIG.copy()
        
    def save(self):
        """Guarda la configuracion actual"""
        try:
            # Asegurar que el directorio existe
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            
            # Actualizar fecha de último acceso
            self.config["last_access"] = datetime.datetime.now().isoformat()
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error al guardar configuracion: {e}")
            return False
            
    def get(self, key, default=None):
        """Obtiene un valor de configuracion"""
        return self.config.get(key, default)
        
    def set(self, key, value):
        """Establece un valor de configuracion"""
        self.config[key] = value
        return self.save()
    
    def add_recent_service(self, service):
        """Agrega un servicio a la lista de recientes"""
        recent = self.config.get("recent_services", [])
        
        # Eliminar si ya existe para evitar duplicados
        if service in recent:
            recent.remove(service)
        
        # Agregar al inicio
        recent.insert(0, service)
        
        # Mantener solo los últimos 10
        self.config["recent_services"] = recent[:10]
        self.save()
    
    def get_vault_path(self):
        """Obtiene la ruta del almacen de contrasenas"""
        vault_path = self.get("vault_path")
        
        # Si es una ruta relativa, hacerla relativa al directorio raíz
        if not os.path.isabs(vault_path):
            vault_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                vault_path
            )
        
        return vault_path