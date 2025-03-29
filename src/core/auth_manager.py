#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestor de autenticacion y claves
"""

import os
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class AuthManager:
    """Gestiona la autenticacion y claves de cifrado"""
    
    def __init__(self):
        """Inicializa el gestor de autenticacion"""
        self.master_key = None
        self.data_key = None
    
    def set_keys(self, master_key, data_key):
        """Establece las claves proporcionadas por el usuario"""
        self.master_key = master_key
        self.data_key = data_key
    
    def get_master_key(self):
        """Obtiene la clave maestra derivada"""
        if self.master_key is None:
            raise ValueError("Las claves no han sido establecidas")
            
        # Derivar clave usando SHA-256 directamente - NO usa salt
        key = hashlib.sha256(self.master_key.encode('utf-8')).digest()
        return key
    
    def get_data_key(self):
        """Obtiene la clave de datos derivada"""
        if self.data_key is None:
            raise ValueError("Las claves no han sido establecidas")
            
        # Derivar clave usando SHA-256 directamente - NO usa salt
        key = hashlib.sha256(self.data_key.encode('utf-8')).digest()
        return key
    
    def encrypt_with_master_key(self, data):
        """
        Cifra datos con la clave maestra
        
        Args:
            data (bytes): Datos a cifrar
            
        Returns:
            bytes: Datos cifrados (formato: iv + datos cifrados)
        """
        if self.master_key is None:
            raise ValueError("Las claves no han sido establecidas")
            
        key = self.get_master_key()
        iv = os.urandom(16)  # Vector de inicializacion (IV)
        
        # Crear cifrador AES en modo CBC con padding
        cipher = AES.new(key, AES.MODE_CBC, iv)
        
        # Cifrar datos con padding
        encrypted_data = cipher.encrypt(pad(data, AES.block_size))
        
        # Combinar IV y datos cifrados
        return iv + encrypted_data
    
    def decrypt_with_master_key(self, encrypted_data):
        """
        Descifra datos con la clave maestra
        
        Args:
            encrypted_data (bytes): Datos cifrados (formato: iv + datos cifrados)
            
        Returns:
            bytes: Datos descifrados
        """
        if self.master_key is None:
            raise ValueError("Las claves no han sido establecidas")
            
        key = self.get_master_key()
        
        # Extraer IV (primeros 16 bytes)
        iv = encrypted_data[:16]
        encrypted_data = encrypted_data[16:]
        
        # Crear descifrador AES en modo CBC
        cipher = AES.new(key, AES.MODE_CBC, iv)
        
        # Descifrar datos y quitar padding
        try:
            return unpad(cipher.decrypt(encrypted_data), AES.block_size)
        except Exception as e:
            raise ValueError("Error al descifrar datos. Clave incorrecta.") from e
    
    def encrypt_with_data_key(self, data):
        """
        Cifra datos con la clave de datos
        
        Args:
            data (bytes): Datos a cifrar
            
        Returns:
            bytes: Datos cifrados (formato: iv + datos cifrados)
        """
        if self.data_key is None:
            raise ValueError("Las claves no han sido establecidas")
            
        key = self.get_data_key()
        iv = os.urandom(16)  # Vector de inicializacion (IV)
        
        # Crear cifrador AES en modo CBC con padding
        cipher = AES.new(key, AES.MODE_CBC, iv)
        
        # Cifrar datos con padding
        encrypted_data = cipher.encrypt(pad(data, AES.block_size))
        
        # Combinar IV y datos cifrados
        return iv + encrypted_data
    
    def decrypt_with_data_key(self, encrypted_data):
        """
        Descifra datos con la clave de datos
        
        Args:
            encrypted_data (bytes): Datos cifrados (formato: iv + datos cifrados)
            
        Returns:
            bytes: Datos descifrados
        """
        if self.data_key is None:
            raise ValueError("Las claves no han sido establecidas")
            
        key = self.get_data_key()
        
        # Extraer IV (primeros 16 bytes)
        iv = encrypted_data[:16]
        encrypted_data = encrypted_data[16:]
        
        # Crear descifrador AES en modo CBC
        cipher = AES.new(key, AES.MODE_CBC, iv)
        
        # Descifrar datos y quitar padding
        try:
            return unpad(cipher.decrypt(encrypted_data), AES.block_size)
        except Exception as e:
            raise ValueError("Error al descifrar datos. Clave incorrecta.") from e
    
    def clear_keys(self):
        """Limpia las claves de la memoria"""
        self.master_key = None
        self.data_key = None
    
    def test_encryption(self):
        """
        Prueba el sistema de cifrado para verificar que las claves funcionan
        
        Returns:
            bool: True si el cifrado/descifrado funciona correctamente
        """
        try:
            # Crear datos de prueba
            test_data = b"Este es un mensaje de prueba para verificar el cifrado."
            
            # Probar cifrado con clave maestra
            encrypted_master = self.encrypt_with_master_key(test_data)
            decrypted_master = self.decrypt_with_master_key(encrypted_master)
            
            # Probar cifrado con clave de datos
            encrypted_data = self.encrypt_with_data_key(test_data)
            decrypted_data = self.decrypt_with_data_key(encrypted_data)
            
            # Verificar que los datos descifrados coincidan con los originales
            return (test_data == decrypted_master) and (test_data == decrypted_data)
        except Exception:
            return False