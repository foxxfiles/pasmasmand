# Gestor de Contrasenas Seguras

Sistema de gestion de contrasenas con cifrado AES256 y almacenamiento local seguro.

## Caracteristicas

- Almacenamiento cifrado con AES256
- Doble nivel de cifrado
- Generador de contrasenas conigurable
- Interfaz grafica intuitiva con tema oscuro
- Sin persistencia de datos en texto plano

## Instalacion

1. Clonar este repositorio
2. Instalar dependencias: `pip install -r requirements.txt`
3. Ejecutar la aplicacion: `python main.py`

## Uso

La aplicacion requerira dos claves al inicio:
- Clave maestra para cifrar el archivo JSON
- Clave secundaria para cifrar los datos dentro del JSON

## Seguridad

Todas las contrasenas se almacenan cifradas y solo se descifran en memoria cuando se necesitan.
