#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Almacen de contrasenas cifradas
"""

import os
import json
import time
import uuid
import base64
import traceback
from datetime import datetime

class PasswordVault:
    """Gestiona el almacenamiento seguro de contrasenas"""
    
    def __init__(self, auth_manager, config):
        """
        Inicializa el almacen de contrasenas
        
        Args:
            auth_manager: Instancia de AuthManager para cifrado/descifrado
            config: Instancia de Config para obtener configuracion
        """
        self.auth_manager = auth_manager
        self.config = config
        self.vault_path = config.get_vault_path()
        self.data = None
    
    def exists(self):
        """
        Comprueba si existe el archivo del almacen
        
        Returns:
            bool: True si el almacen existe
        """
        return os.path.exists(self.vault_path) and os.path.getsize(self.vault_path) > 0
    
    def initialize_vault(self):
        """
        Crea un nuevo almacen vacio
        
        Returns:
            bool: True si se creo correctamente
        """
        # Estructura inicial del almacen
        vault_data = {
            "metadata": {
                "version": "1.0",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "description": "Almacen de contrasenas cifradas"
            },
            "passwords": []
        }
        
        # Convertir a JSON y cifrar
        return self.save(vault_data)
    
    def test_keys(self):
        """
        Prueba si las claves pueden descifrar el almacen
        
        Returns:
            bool: True si las claves son correctas
        """
        try:
            # Intentar cargar el almacen
            print("DEBUG: Intentando cargar almacén en test_keys()")
            self.load()
            print("DEBUG: Almacén cargado correctamente en test_keys()")
            return True
        except Exception as e:
            print(f"DEBUG: Error en test_keys(): {str(e)}")
            print(traceback.format_exc())
            return False
    
    def load(self):
        """
        Carga el almacen cifrado desde el disco
        
        Returns:
            dict: Datos del almacen
            
        Raises:
            ValueError: Si hay un error al descifrar o el archivo no existe
        """
        # Verificar que el archivo existe
        if not self.exists():
            print("DEBUG: El almacén no existe en load()")
            raise ValueError("No se encontró un almacén de contraseñas")
        
        try:
            # Leer archivo cifrado
            print(f"DEBUG: Leyendo archivo cifrado desde {self.vault_path}")
            with open(self.vault_path, 'rb') as f:
                encrypted_data = f.read()
            
            print(f"DEBUG: Leídos {len(encrypted_data)} bytes de datos cifrados")
            
            # Descifrar con clave maestra
            print("DEBUG: Intentando descifrar con clave maestra")
            json_data = self.auth_manager.decrypt_with_master_key(encrypted_data)
            
            print(f"DEBUG: Datos descifrados exitosamente, longitud: {len(json_data)}")
            
            # Convertir de JSON a diccionario
            vault_data = json.loads(json_data.decode('utf-8'))
            
            print("DEBUG: JSON decodificado correctamente")
            
            # Almacenar en memoria
            self.data = vault_data
            return vault_data
            
        except Exception as e:
            print(f"DEBUG: Error en load(): {str(e)}")
            print(traceback.format_exc())
            raise ValueError(f"Error al cargar el almacén: {str(e)}")
    
    def save(self, data=None):
        """
        Guarda datos cifrados en el almacen
        
        Args:
            data (dict, opcional): Datos a guardar. Si es None, guarda self.data
            
        Returns:
            bool: True si se guardó correctamente
            
        Raises:
            ValueError: Si hay un error al cifrar o guardar
        """
        try:
            # Usar datos proporcionados o los cargados previamente
            if data is None:
                if self.data is None:
                    raise ValueError("No hay datos para guardar")
                data = self.data
            
            # Actualizar fecha de modificación
            data["metadata"]["updated_at"] = datetime.now().isoformat()
            
            # Convertir a JSON
            json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')
            
            print(f"DEBUG: Convertido a JSON, longitud: {len(json_data)}")
            
            # Cifrar con clave maestra
            encrypted_data = self.auth_manager.encrypt_with_master_key(json_data)
            
            print(f"DEBUG: Datos cifrados con clave maestra, longitud: {len(encrypted_data)}")
            
            # Asegurar que el directorio existe
            os.makedirs(os.path.dirname(os.path.abspath(self.vault_path)), exist_ok=True)
            
            # Guardar en archivo
            with open(self.vault_path, 'wb') as f:
                f.write(encrypted_data)
            
            print(f"DEBUG: Datos cifrados guardados en {self.vault_path}")
            
            # Actualizar datos en memoria
            self.data = data
            return True
            
        except Exception as e:
            print(f"DEBUG: Error en save(): {str(e)}")
            print(traceback.format_exc())
            raise ValueError(f"Error al guardar el almacén: {str(e)}")
    
    # El resto del código permanece igual...
    def get_all_passwords(self):
        """
        Obtiene todas las entradas de contrasenas
        
        Returns:
            list: Lista de entradas descifradas
        """
        # Cargar datos si no están en memoria
        if self.data is None:
            self.load()
        
        # Lista para almacenar entradas descifradas
        decrypted_entries = []
        
        # Procesar cada entrada
        for entry in self.data.get("passwords", []):
            try:
                # Descifrar cada campo con la clave de datos
                decrypted_entry = self._decrypt_entry(entry)
                decrypted_entries.append(decrypted_entry)
            except Exception as e:
                print(f"Error al descifrar entrada {entry.get('id', 'desconocido')}: {str(e)}")
        
        return decrypted_entries
    
    def add_password(self, entry_data):
        """
        Agrega una nueva entrada de contrasena
        
        Args:
            entry_data (dict): Datos de la entrada
            
        Returns:
            str: ID de la entrada creada
        """
        # Cargar datos si no están en memoria
        if self.data is None:
            self.load()
        
        # Generar ID único
        entry_id = str(uuid.uuid4())
        
        # Crear estructura de entrada
        entry = {
            "id": entry_id,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # Cifrar campos con la clave de datos
        encrypted_entry = self._encrypt_entry(entry_data, entry)
        
        # Agregar a la lista de contraseñas
        self.data["passwords"].append(encrypted_entry)
        
        # Guardar cambios
        self.save()
        
        return entry_id
    
    def update_password(self, entry_id, entry_data):
        """
        Actualiza una entrada existente
        
        Args:
            entry_id (str): ID de la entrada a actualizar
            entry_data (dict): Nuevos datos
            
        Returns:
            bool: True si se actualizó correctamente
            
        Raises:
            ValueError: Si la entrada no existe
        """
        # Cargar datos si no están en memoria
        if self.data is None:
            self.load()
        
        # Buscar la entrada por ID
        for i, entry in enumerate(self.data["passwords"]):
            if entry["id"] == entry_id:
                # Mantener datos originales que no se deben cambiar
                original = entry.copy()
                original["updated_at"] = datetime.now().isoformat()
                
                # Cifrar nuevos datos
                updated_entry = self._encrypt_entry(entry_data, original)
                
                # Actualizar entrada
                self.data["passwords"][i] = updated_entry
                
                # Guardar cambios
                self.save()
                return True
        
        # La entrada no existe
        raise ValueError(f"No se encontró una entrada con ID '{entry_id}'")
    
    def delete_password(self, entry_id):
        """
        Elimina una entrada de contrasena
        
        Args:
            entry_id (str): ID de la entrada a eliminar
            
        Returns:
            bool: True si se eliminó correctamente
        """
        # Cargar datos si no están en memoria
        if self.data is None:
            self.load()
        
        # Buscar y eliminar la entrada
        for i, entry in enumerate(self.data["passwords"]):
            if entry["id"] == entry_id:
                # Eliminar de la lista
                del self.data["passwords"][i]
                
                # Guardar cambios
                self.save()
                return True
        
        return False
    
    def get_password(self, entry_id):
        """
        Obtiene una entrada de contrasena por ID
        
        Args:
            entry_id (str): ID de la entrada
            
        Returns:
            dict: Datos descifrados de la entrada
            
        Raises:
            ValueError: Si la entrada no existe
        """
        # Cargar datos si no están en memoria
        if self.data is None:
            self.load()
        
        # Buscar la entrada por ID
        for entry in self.data["passwords"]:
            if entry["id"] == entry_id:
                # Descifrar y retornar
                return self._decrypt_entry(entry)
        
        # La entrada no existe
        raise ValueError(f"No se encontró una entrada con ID '{entry_id}'")
    
    def search_passwords(self, query):
        """
        Busca entradas que coincidan con el criterio
        
        Args:
            query (str): Texto a buscar
            
        Returns:
            list: Entradas que coinciden
        """
        # Obtener todas las entradas descifradas
        all_entries = self.get_all_passwords()
        query = query.lower()
        
        # Filtrar por coincidencia en cualquier campo
        results = []
        for entry in all_entries:
            if (query in entry.get("username", "").lower() or
                query in entry.get("service", "").lower() or
                query in entry.get("comment", "").lower()):
                results.append(entry)
        
        return results
    
    def _encrypt_entry(self, entry_data, base_entry=None):
        """
        Cifra los campos de una entrada
        
        Args:
            entry_data (dict): Datos a cifrar
            base_entry (dict, opcional): Entrada base para mantener metadatos
            
        Returns:
            dict: Entrada con campos cifrados
        """
        # Usar base proporcionada o crear nueva
        encrypted_entry = base_entry or {
            "id": str(uuid.uuid4()),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # Cifrar cada campo individual
        for field in ["username", "service", "password", "comment"]:
            if field in entry_data and entry_data[field]:
                # Convertir a bytes
                field_data = entry_data[field].encode('utf-8')
                
                # Cifrar con clave de datos
                encrypted_field = self.auth_manager.encrypt_with_data_key(field_data)
                
                # Convertir a base64 para almacenamiento
                encrypted_entry[field] = base64.b64encode(encrypted_field).decode('utf-8')
        
        return encrypted_entry
    
    def _decrypt_entry(self, encrypted_entry):
        """
        Descifra los campos de una entrada
        
        Args:
            encrypted_entry (dict): Entrada con campos cifrados
            
        Returns:
            dict: Entrada con campos descifrados
        """
        decrypted_entry = {
            "id": encrypted_entry["id"],
            "created_at": encrypted_entry["created_at"],
            "updated_at": encrypted_entry["updated_at"]
        }
        
        # Descifrar cada campo
        for field in ["username", "service", "password", "comment"]:
            if field in encrypted_entry and encrypted_entry[field]:
                try:
                    # Convertir de base64 a bytes
                    encrypted_field = base64.b64decode(encrypted_entry[field])
                    
                    # Descifrar con clave de datos
                    decrypted_field = self.auth_manager.decrypt_with_data_key(encrypted_field)
                    
                    # Convertir a texto
                    decrypted_entry[field] = decrypted_field.decode('utf-8')
                except Exception as e:
                    print(f"Error al descifrar campo {field}: {str(e)}")
                    decrypted_entry[field] = f"[Error: No se pudo descifrar]"
        
        return decrypted_entry