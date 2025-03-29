#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de contrasenas seguras
"""

import string
import secrets
import re
import math

class PasswordGenerator:
    """Generador de contrasenas configurable y seguro"""
    
    def __init__(self):
        """Inicializa el generador con configuracion predeterminada"""
        # Configuracion predeterminada
        self.use_lowercase = True
        self.use_uppercase = True
        self.use_digits = True
        self.use_special = True
        self.exclude_similar = False
        self.exclude_ambiguous = False
        self.length = 16
        self.min_length = 4
        self.max_length = 5000
        
        # Conjuntos de caracteres
        self._lowercase = string.ascii_lowercase
        self._uppercase = string.ascii_uppercase
        self._digits = string.digits
        self._special = "!@#$%^&*()-_=+[]{}|;:,.<>?/~"
        self._similar = "il1Lo0O"
        self._ambiguous = "`'\"\\"
        
    def configure(self, **options):
        """
        Configura las opciones del generador
        
        Args:
            **options: Opciones a configurar (use_lowercase, use_uppercase, etc.)
            
        Returns:
            self: Para permitir encadenamiento de metodos
        """
        # Actualizar opciones proporcionadas
        for option, value in options.items():
            if hasattr(self, option):
                setattr(self, option, value)
        
        # Validar longitud
        self.length = max(self.min_length, min(self.length, self.max_length))
        
        return self
    
    def generate(self):
        """
        Genera una contrasena con la configuracion actual
        
        Returns:
            str: Contrasena generada
            
        Raises:
            ValueError: Si no hay caracteres disponibles para generar la contrasena
        """
        # Construir conjunto de caracteres segun configuracion
        char_pool = ""
        
        if self.use_lowercase:
            char_pool += self._lowercase
        
        if self.use_uppercase:
            char_pool += self._uppercase
        
        if self.use_digits:
            char_pool += self._digits
        
        if self.use_special:
            char_pool += self._special
        
        # Eliminar caracteres similares si esta configurado
        if self.exclude_similar:
            for char in self._similar:
                char_pool = char_pool.replace(char, "")
        
        # Eliminar caracteres ambiguos si esta configurado
        if self.exclude_ambiguous:
            for char in self._ambiguous:
                char_pool = char_pool.replace(char, "")
        
        # Verificar que haya caracteres disponibles
        if not char_pool:
            raise ValueError("No hay caracteres disponibles para generar la contraseña")
        
        # Si la longitud es muy grande, usar algoritmo optimizado
        if self.length > 1000:
            return self._generate_large_password(char_pool)
        
        # Generar contraseña asegurando que cumpla con los requisitos
        while True:
            # Usar secrets para generacion criptograficamente segura
            password = ''.join(secrets.choice(char_pool) for _ in range(self.length))
            
            # Verificar que la contraseña cumple con todos los requisitos habilitados
            if self._validate_password(password):
                return password
    
    def _generate_large_password(self, char_pool):
        """
        Genera una contrasena muy larga de manera eficiente
        
        Args:
            char_pool (str): Conjunto de caracteres a utilizar
            
        Returns:
            str: Contrasena generada
        """
        # Para contraseñas extremadamente largas, generamos por bloques
        # y aseguramos que al menos un bloque cumple con cada requisito
        block_size = 1000
        num_blocks = (self.length + block_size - 1) // block_size
        
        password = ""
        
        for i in range(num_blocks):
            # Calcular tamaño del bloque actual (el último puede ser más pequeño)
            current_block_size = min(block_size, self.length - len(password))
            
            # Generar bloque
            block = ''.join(secrets.choice(char_pool) for _ in range(current_block_size))
            
            # Si es el primer bloque, asegurar que cumple con los requisitos
            if i == 0:
                while not self._validate_password(block):
                    block = ''.join(secrets.choice(char_pool) for _ in range(current_block_size))
            
            password += block
        
        return password
    
    def _validate_password(self, password):
        """
        Verifica que la contrasena cumple con los requisitos configurados
        
        Args:
            password (str): Contrasena a validar
            
        Returns:
            bool: True si cumple con todos los requisitos activos
        """
        # Verificar requisitos solo si están habilitados
        if self.use_lowercase and not re.search(r'[a-z]', password):
            return False
        
        if self.use_uppercase and not re.search(r'[A-Z]', password):
            return False
        
        if self.use_digits and not re.search(r'\d', password):
            return False
        
        if self.use_special and not any(c in self._special for c in password):
            return False
        
        return True
    
    def get_entropy(self, password=None):
        """
        Calcula la entropia (fortaleza) de la contrasena
        
        Args:
            password (str, opcional): Contrasena a evaluar. Si no se proporciona,
                                     usa la configuracion actual para estimar.
            
        Returns:
            float: Entropia en bits
        """
        # Si no se proporciona contraseña, calcular entropia potencial
        if password is None:
            # Calcular tamaño del conjunto de caracteres
            pool_size = 0
            if self.use_lowercase:
                pool_size += len(self._lowercase)
            if self.use_uppercase:
                pool_size += len(self._uppercase)
            if self.use_digits:
                pool_size += len(self._digits)
            if self.use_special:
                pool_size += len(self._special)
                
            # Eliminar caracteres similares o ambiguos si está configurado
            if self.exclude_similar:
                pool_size -= sum(1 for c in self._similar if c in (
                    self._lowercase + self._uppercase + self._digits + self._special
                ))
            if self.exclude_ambiguous:
                pool_size -= sum(1 for c in self._ambiguous if c in (
                    self._lowercase + self._uppercase + self._digits + self._special
                ))
                
            # Fórmula de entropía = longitud * log2(tamaño del conjunto)
            if pool_size <= 1:
                return 0
            return self.length * math.log2(pool_size)
        else:
            # Calcular entropía real de la contraseña proporcionada
            # mediante análisis de caracteres utilizados
            char_set = set()
            if any(c in string.ascii_lowercase for c in password):
                char_set.update(string.ascii_lowercase)
            if any(c in string.ascii_uppercase for c in password):
                char_set.update(string.ascii_uppercase)
            if any(c in string.digits for c in password):
                char_set.update(string.digits)
            if any(c in self._special for c in password):
                char_set.update(self._special)
            
            if len(char_set) <= 1:
                return 0
            return len(password) * math.log2(len(char_set))
    
    def get_strength_description(self, entropy=None):
        """
        Obtiene una descripcion de la fortaleza de la contrasena
        
        Args:
            entropy (float, opcional): Entropia en bits. Si no se proporciona,
                                      usa la configuracion actual para estimar.
            
        Returns:
            str: Descripcion de la fortaleza
        """
        if entropy is None:
            entropy = self.get_entropy()
        
        if entropy < 28:
            return "Muy débil"
        elif entropy < 36:
            return "Débil"
        elif entropy < 60:
            return "Razonable"
        elif entropy < 128:
            return "Fuerte"
        else:
            return "Muy fuerte"
    
    def generate_memorable(self, num_words=4):
        """
        Genera una contrasena memorable usando palabras aleatorias
        
        Args:
            num_words (int): Numero de palabras a utilizar
            
        Returns:
            str: Contrasena generada
        """
        # Lista de palabras comunes en español (limitadas a longitud 5-8)
        palabras = [
            "casa", "agua", "vida", "tiempo", "mundo", "forma", "parte", "lugar",
            "libro", "hora", "mujer", "punto", "grupo", "igual", "crear", "color",
            "norte", "papel", "cinco", "habla", "poder", "jugar", "hacer", "media",
            "carta", "playa", "clase", "fecha", "joven", "noche", "campo", "largo",
            "valor", "serie", "mesa", "mejor", "final", "claro", "vista", "linea",
            "reino", "orden", "fuego", "tierra", "saber", "pared", "falta", "dejar"
        ]
        
        # Seleccionar palabras aleatorias
        selected_words = [secrets.choice(palabras) for _ in range(num_words)]
        
        # Agregar un número aleatorio al final
        num = secrets.randbelow(1000)
        
        # Agregar un carácter especial aleatorio
        special_char = secrets.choice(self._special)
        
        # Construir contraseña combinando palabras, número y carácter especial
        # Aplicar mayúscula a la primera letra de cada palabra
        password = ''.join(word.capitalize() for word in selected_words)
        password += str(num) + special_char
        
        return password