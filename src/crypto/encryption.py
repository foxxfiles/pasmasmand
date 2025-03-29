#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor de cifrado AES256
"""

import os
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

class CryptoEngine:
    """Motor de cifrado y descifrado con AES256"""
    
    def __init__(self):
        """Inicializa el motor de cifrado"""
        # No almacenar claves como atributos de instancia
        # para evitar persistencia innecesaria en memoria
        pass
    
    def derive_key(self, password, salt=None, iterations=1000000):
        """
        Deriva una clave criptografica a partir de una contraseña
        
        Args:
            password (str): Contraseña de entrada
            salt (bytes, opcional): Salt para PBKDF2. Si es None, genera uno nuevo
            iterations (int): Número de iteraciones para PBKDF2
            
        Returns:
            tuple: (clave_derivada, salt)
        """
        # Generar salt si no se proporciona
        if salt is None:
            salt = get_random_bytes(16)
        
        # Asegurar que password sea bytes
        if isinstance(password, str):
            password = password.encode('utf-8')
        
        # Derivar clave usando PBKDF2 con SHA-256
        key = PBKDF2(
            password, 
            salt, 
            dkLen=32,  # 32 bytes = 256 bits para AES-256
            count=iterations,
            hmac_hash_module=hashlib.sha256
        )
        
        return (key, salt)
    
    def encrypt(self, data, key):
        """
        Cifra datos con AES-256 en modo CBC
        
        Args:
            data: Datos a cifrar (str o bytes)
            key: Clave de cifrado (bytes)
            
        Returns:
            bytes: Datos cifrados (formato: iv + datos_cifrados)
            
        Raises:
            ValueError: Si hay error en el cifrado
        """
        try:
            # Convertir datos a bytes si es necesario
            if isinstance(data, str):
                data = data.encode('utf-8')
            
            # Generar vector de inicialización (IV)
            iv = get_random_bytes(16)
            
            # Crear cifrador AES en modo CBC
            cipher = AES.new(key, AES.MODE_CBC, iv)
            
            # Aplicar padding y cifrar
            encrypted_data = cipher.encrypt(pad(data, AES.block_size))
            
            # Combinar IV y datos cifrados para almacenamiento
            return iv + encrypted_data
            
        except Exception as e:
            raise ValueError(f"Error en el cifrado: {str(e)}")
    
    def decrypt(self, encrypted_data, key):
        """
        Descifra datos con AES-256 en modo CBC
        
        Args:
            encrypted_data (bytes): Datos cifrados (formato: iv + datos_cifrados)
            key (bytes): Clave de descifrado
            
        Returns:
            bytes: Datos descifrados
            
        Raises:
            ValueError: Si hay error en el descifrado
        """
        try:
            # Extraer IV (primeros 16 bytes)
            iv = encrypted_data[:16]
            ciphertext = encrypted_data[16:]
            
            # Crear descifrador AES en modo CBC
            cipher = AES.new(key, AES.MODE_CBC, iv)
            
            # Descifrar y quitar padding
            return unpad(cipher.decrypt(ciphertext), AES.block_size)
            
        except Exception as e:
            raise ValueError(f"Error en el descifrado: {str(e)}")
    
    def encrypt_to_b64(self, data, key):
        """
        Cifra datos y los convierte a string Base64
        
        Args:
            data: Datos a cifrar
            key: Clave de cifrado
            
        Returns:
            str: Datos cifrados en formato Base64
        """
        encrypted = self.encrypt(data, key)
        return base64.b64encode(encrypted).decode('utf-8')
    
    def decrypt_from_b64(self, b64_data, key):
        """
        Descifra datos en formato Base64
        
        Args:
            b64_data (str): Datos cifrados en Base64
            key: Clave de descifrado
            
        Returns:
            bytes: Datos descifrados
        """
        encrypted = base64.b64decode(b64_data)
        return self.decrypt(encrypted, key)
    
    def hash_password(self, password, salt=None):
        """
        Crea un hash seguro de una contraseña
        
        Args:
            password (str): Contraseña a hashear
            salt (bytes, opcional): Salt para el hash
            
        Returns:
            tuple: (hash, salt)
        """
        if salt is None:
            salt = get_random_bytes(16)
            
        if isinstance(password, str):
            password = password.encode('utf-8')
            
        # Usar PBKDF2 para crear un hash seguro
        password_hash = PBKDF2(
            password, 
            salt, 
            dkLen=32,
            count=100000,
            hmac_hash_module=hashlib.sha256
        )
        
        return (password_hash, salt)
    
    def verify_password(self, password, stored_hash, salt):
        """
        Verifica si una contraseña coincide con un hash almacenado
        
        Args:
            password (str): Contraseña a verificar
            stored_hash (bytes): Hash almacenado
            salt (bytes): Salt usado para el hash
            
        Returns:
            bool: True si la contraseña coincide
        """
        password_hash, _ = self.hash_password(password, salt)
        return password_hash == stored_hash
    
    def generate_key(self):
        """
        Genera una clave aleatoria para AES-256
        
        Returns:
            bytes: Clave aleatoria de 32 bytes (256 bits)
        """
        return get_random_bytes(32)
    
    @staticmethod
    def secure_delete(variable):
        """
        Intenta eliminar de forma segura una variable de la memoria
        
        Args:
            variable: Variable a eliminar
        """
        if isinstance(variable, bytes):
            # Sobrescribir con bytes aleatorios
            for i in range(len(variable)):
                try:
                    variable[i] = 0
                except:
                    # Algunas implementaciones de bytes son inmutables
                    pass
        
        # Intentar eliminar el objeto
        del variable