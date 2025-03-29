# Secure Password Manager

A robust desktop password management system with AES-256 encryption and secure local storage.


## Features

- **Strong Encryption**: All data secured with AES-256 encryption
- **Dual-Layer Security**: Two separate keys required to access your passwords
- **Zero Plaintext Storage**: No passwords ever stored in plaintext
- **Password Generator**: Create strong passwords with configurable settings
- **QR Code Generation**: Export secure credentials as QR codes for easy mobile transfer
- **Dark Mode Interface**: Eye-friendly design for extended use
- **Clipboard Management**: Auto-clearing clipboard after copying sensitive data
- **Password Strength Analysis**: Real-time feedback on password security
- **Search Functionality**: Quickly find credentials by service or username
- **Portable**: No external servers or cloud dependencies, perfect for offline use
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Screenshots

<div align="center">
  <img src="https://github.com/foxxfiles/pasmasmand/blob/main/images/passman3.png" alt="Login Screen" width="400">
  <img src="https://github.com/foxxfiles/pasmasmand/blob/main/images/passman2.png" alt="Password Generator" width="400">
  <img src="https://github.com/foxxfiles/pasmasmand/blob/main/images/passman1.png" alt="QR Code Export" width="400">
</div>

## Requirements

- Python 3.7 or higher
- tkinter (usually bundled with Python)
- PyCryptodome 3.15.0 or higher
- ttkbootstrap 1.0.0 or higher

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/secure-password-manager.git
cd secure-password-manager
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Usage

### First Time Setup

When starting the application for the first time:

1. Check the "Create new password vault" checkbox
2. Set your Master Key (used to encrypt the vault file)
3. Set your Data Key (used to encrypt individual entries)
4. Click "Access" to create your vault

**IMPORTANT**: Remember both keys! If lost, your data cannot be recovered.

### Managing Passwords

- **Add Password**: Click the "New" button to add a new password entry
- **Edit Password**: Select an entry and click "Edit" to modify its details
- **Delete Password**: Select an entry and click "Delete" to remove it
- **Generate Password**: Click the "Generate" button to create a secure password
- **QR Code**: In the entry view, click "Generate QR" to create a QR code of your credentials

### Security Features

- Auto logout after 5 minutes of inactivity (configurable)
- Maximum login attempts limit (default: 5)
- Clipboard automatically cleared 30 seconds after copying sensitive data
- Password strength indicator with detailed feedback

## How It Works

The application uses a dual-layer encryption system:

1. **Outer Layer**: Your entire password vault is encrypted with your Master Key
2. **Inner Layer**: Each individual password entry is encrypted with your Data Key

This dual-layer approach ensures that even if one key is compromised, your passwords remain protected.

## Security Considerations

- All encryption is performed locally using industry-standard AES-256
- No plaintext data is ever stored on disk
- Secure memory handling minimizes the risk of sensitive data exposure
- No network communication or telemetry

## Development

### Project Structure

```
# Estructura del Proyecto PasMan (Gestor de Contraseñas Seguras)

pasman/
├── .gitignore
├── README.md
├── empty_vault
├── main.py                # Punto de entrada principal de la aplicación
├── main.spec              # Archivo de especificación para PyInstaller
├── requirements.txt       # Dependencias del proyecto
├── estructura_proyecto.txt  # Este archivo
│
│
├── src/                   # Código fuente principal
│   ├── __init__.py
│   │
│   ├── core/              # Funcionalidad principal
│   │   ├── __init__.py
│   │   ├── auth_manager.py         # Gestión de autenticación
│   │   ├── password_generator.py   # Generador de contraseñas
│   │   └── password_manager.py     # Gestor de contraseñas
│   │
│   ├── crypto/            # Módulos de criptografía
│   │   ├── __init__.py
│   │   └── encryption.py            # Implementación de cifrado AES256
│   │
│   ├── storage/           # Almacenamiento de datos
│   │   ├── __init__.py
│   │   └── vault.py                 # Gestión del almacén de contraseñas
│   │
│   ├── ui/                # Interfaz de usuario
│   │   ├── __init__.py
│   │   ├── login_window.py          # Ventana de inicio de sesión
│   │   ├── main_window.py           # Ventana principal
│   │   ├── password_entry_dialog.py # Diálogo para entrada de contraseñas
│   │   └── password_generator_dialog.py # Diálogo del generador de contraseñas
│   │
│   └── utils/             # Utilidades
│       ├── __init__.py
│       ├── config.py                # Gestión de configuración
│       └── pyinstaller_utils.py     # Utilidades para PyInstaller
│
└── tests/                 # Pruebas unitarias y de integración
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [PyCryptodome](https://pycryptodome.readthedocs.io/) for cryptographic functions
- [ttkbootstrap](https://ttkbootstrap.readthedocs.io/) for the modern UI theme
- All contributors who have helped make this project better
