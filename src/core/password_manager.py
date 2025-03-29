#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestor principal de contrasenas
"""

import time
import uuid
from datetime import datetime
import re

class PasswordManager:
    """Gestiona las operaciones con contrasenas"""
    
    def __init__(self, vault):
        """
        Inicializa el gestor de contrasenas
        
        Args:
            vault: Instancia de PasswordVault para almacenamiento
        """
        self.vault = vault
        self.passwords = []
        self.cached_search = None
    
    def get_all_passwords(self):
        """
        Obtiene todas las entradas de contrasenas
        
        Returns:
            list: Lista de entradas
        """
        try:
            return self.vault.get_all_passwords()
        except Exception as e:
            # Relanzar con mensaje más descriptivo
            raise RuntimeError(f"Error al obtener contraseñas: {str(e)}") from e
    
    def add_password(self, entry_data):
        """
        Agrega una nueva entrada de contrasena
        
        Args:
            entry_data (dict): Datos de la entrada (username, service, password, comment)
            
        Returns:
            str: ID de la entrada creada
            
        Raises:
            ValueError: Si faltan datos requeridos
        """
        # Validar campos requeridos
        self._validate_required_fields(entry_data)
        
        # Validar que la contraseña no esté vacía
        if not entry_data.get("password"):
            raise ValueError("La contraseña no puede estar vacía")
        
        try:
            # Agregar al almacén
            entry_id = self.vault.add_password(entry_data)
            
            # Limpiar caché de búsqueda
            self.cached_search = None
            
            return entry_id
        except Exception as e:
            # Relanzar con mensaje más descriptivo
            raise RuntimeError(f"Error al agregar contraseña: {str(e)}") from e
    
    def update_password(self, entry_id, updated_entry):
        """
        Actualiza una entrada existente
        
        Args:
            entry_id (str): ID de la entrada a actualizar
            updated_entry (dict): Nuevos datos
            
        Returns:
            bool: True si se actualizó correctamente
            
        Raises:
            ValueError: Si faltan datos requeridos o el ID no es válido
        """
        # Validar ID
        if not entry_id:
            raise ValueError("Se requiere ID de entrada para actualizar")
        
        # Validar campos requeridos
        self._validate_required_fields(updated_entry)
        
        try:
            # Actualizar en el almacén
            result = self.vault.update_password(entry_id, updated_entry)
            
            # Limpiar caché de búsqueda
            self.cached_search = None
            
            return result
        except Exception as e:
            # Relanzar con mensaje más descriptivo
            raise RuntimeError(f"Error al actualizar contraseña: {str(e)}") from e
    
    def delete_password(self, entry_id):
        """
        Elimina una entrada de contrasena
        
        Args:
            entry_id (str): ID de la entrada a eliminar
            
        Returns:
            bool: True si se eliminó correctamente
            
        Raises:
            ValueError: Si el ID no es válido
        """
        # Validar ID
        if not entry_id:
            raise ValueError("Se requiere ID de entrada para eliminar")
        
        try:
            # Eliminar del almacén
            result = self.vault.delete_password(entry_id)
            
            # Limpiar caché de búsqueda
            self.cached_search = None
            
            return result
        except Exception as e:
            # Relanzar con mensaje más descriptivo
            raise RuntimeError(f"Error al eliminar contraseña: {str(e)}") from e
    
    def get_password(self, entry_id):
        """
        Obtiene una entrada de contrasena por ID
        
        Args:
            entry_id (str): ID de la entrada
            
        Returns:
            dict: Datos de la entrada
            
        Raises:
            ValueError: Si el ID no es válido o no se encuentra
        """
        # Validar ID
        if not entry_id:
            raise ValueError("Se requiere ID de entrada para obtener detalles")
        
        try:
            # Obtener del almacén
            return self.vault.get_password(entry_id)
        except Exception as e:
            # Relanzar con mensaje más descriptivo
            raise RuntimeError(f"Error al obtener contraseña: {str(e)}") from e
    
    def search_passwords(self, query):
        """
        Busca entradas que coincidan con el criterio
        
        Args:
            query (str): Texto a buscar
            
        Returns:
            list: Entradas que coinciden
        """
        if not query:
            # Si no hay consulta, devolver todas
            return self.get_all_passwords()
        
        try:
            # Realizar búsqueda en el almacén
            results = self.vault.search_passwords(query)
            
            # Guardar resultados en caché
            self.cached_search = {
                "query": query,
                "results": results,
                "timestamp": time.time()
            }
            
            return results
        except Exception as e:
            # Relanzar con mensaje más descriptivo
            raise RuntimeError(f"Error al buscar contraseñas: {str(e)}") from e
    
    def check_password_strength(self, password):
        """
        Evalúa la fortaleza de una contraseña
        
        Args:
            password (str): Contraseña a evaluar
            
        Returns:
            dict: Información de fortaleza (score, feedback)
        """
        if not password:
            return {
                "score": 0,
                "feedback": "La contraseña está vacía"
            }
        
        # Iniciar puntuación
        score = 0
        feedback = []
        
        # Longitud (0-5 puntos)
        length = len(password)
        if length < 8:
            score += 0
            feedback.append("Demasiado corta")
        elif length < 10:
            score += 1
        elif length < 12:
            score += 2
        elif length < 14:
            score += 3
        elif length < 16:
            score += 4
        else:
            score += 5
        
        # Complejidad (0-5 puntos)
        if re.search(r'[a-z]', password):
            score += 1
        else:
            feedback.append("Falta minúsculas")
            
        if re.search(r'[A-Z]', password):
            score += 1
        else:
            feedback.append("Falta mayúsculas")
            
        if re.search(r'\d', password):
            score += 1
        else:
            feedback.append("Falta números")
            
        if re.search(r'[^a-zA-Z0-9]', password):
            score += 1
        else:
            feedback.append("Falta símbolos")
            
        # Variedad de caracteres (0-1 punto)
        unique_chars = len(set(password))
        if unique_chars > length / 2:
            score += 1
        
        # Normalizar puntuación a escala 0-100
        normalized_score = min(int(score * 10), 100)
        
        # Determinar nivel de fortaleza
        if normalized_score < 30:
            strength = "Muy débil"
        elif normalized_score < 50:
            strength = "Débil"
        elif normalized_score < 70:
            strength = "Moderada"
        elif normalized_score < 90:
            strength = "Fuerte"
        else:
            strength = "Muy fuerte"
        
        return {
            "score": normalized_score,
            "strength": strength,
            "feedback": feedback
        }
    
    def _validate_required_fields(self, entry_data):
        """
        Valida que los campos requeridos estén presentes
        
        Args:
            entry_data (dict): Datos a validar
            
        Raises:
            ValueError: Si faltan campos requeridos
        """
        # Verificar campos requeridos
        if not entry_data.get("service"):
            raise ValueError("El nombre del servicio es requerido")
        
        if not entry_data.get("username"):
            raise ValueError("El nombre de usuario es requerido")