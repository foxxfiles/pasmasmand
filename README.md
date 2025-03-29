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
git clone https://github.com/foxxfiles/pasmasmand
cd passmand
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```
# Instructions to Create PasMan Executable

This document explains how to convert the PasMan (Secure Password Manager) application into a Windows executable using PyInstaller.

## Prerequisites

1. Ensure you have Python 3.6 or higher installed
2. Install all project dependencies:

```bash
pip install -r requirements.txt
pip install pyinstaller
```

## Steps to Create the Executable

### 1. Environment Preparation

Before creating the executable, verify the application works correctly in development mode:

```bash
python main.py
```

### 2. Spec File Configuration

Modify the `main.spec` file to include necessary files in the final executable. Edit `main.spec` to include the `empty_vault` file and other required resources:

```python
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('empty_vault', '.')],  # Include empty_vault in root
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='passman',  # Final executable name
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # False for GUI application without console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='src/ui/assets/icon.ico',  # Optional: Add icon if available
)
```

> **Note**: If you have an application icon file, ensure you specify the correct path in the `icon` parameter. If no icon is available, you can remove that line.

### 3. Executable Creation

After configuring the spec file, run PyInstaller to create the executable:

```bash
pyinstaller main.spec
```

This command will generate the executable in the `dist/` folder.

### 4. Executable Verification

Verify the executable works correctly:
1. Navigate to the `dist/` folder
2. Run `passman.exe`
3. Confirm all application functionalities work properly

### 5. Installer Creation (Optional)

To create a simple installer, you can use tools like NSIS (Nullsoft Scriptable Install System) or Inno Setup.

## Troubleshooting Common Issues

### Problem: Executable can't find vault file

**Solution**: Ensure `empty_vault` is included in the spec file's `datas` parameter and that the `ensure_vault_exists` function in `pyinstaller_utils.py` works correctly.

### Problem: Missing dependencies

**Solution**: If the executable fails due to missing dependencies, explicitly add them in the spec file's `hiddenimports`:

```python
hiddenimports=['Crypto', 'Crypto.Cipher', 'Crypto.Cipher.AES', 'ttkbootstrap'],
```

### Problem: Executable size is too large

**Solution**: Reduce executable size by excluding unnecessary modules in the spec file's `excludes` parameter.

## Executable Distribution

To distribute the application:
1. Create a ZIP file containing the executable and any additional required files:

```bash
powershell Compress-Archive -Path dist\passman.exe -DestinationPath dist\passman.zip
```

2. Distribute the ZIP file or installer (if created)

## Additional Notes
- The created executable is standalone and doesn't require Python installation
- All dependencies are included in the executable
- The application will automatically create an empty vault file on first run if none exists
- Configuration files will be saved in the same directory as the executable

---

Done! You now have a PasMan executable that can be distributed to users without requiring Python or project dependencies installation.
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
├── main.py                         # Punto de entrada principal de la aplicación
├── main.spec                       # Archivo de especificación para PyInstaller
├── requirements.txt                # Dependencias del proyecto
├── estructura_proyecto.txt         # Este archivo
│
│
├── src/                            # Código fuente principal
│   ├── __init__.py
│   │
│   ├── core/                       # Funcionalidad principal
│   │   ├── __init__.py
│   │   ├── auth_manager.py         # Gestión de autenticación
│   │   ├── password_generator.py   # Generador de contraseñas
│   │   └── password_manager.py     # Gestor de contraseñas
│   │
│   ├── crypto/                     # Módulos de criptografía
│   │   ├── __init__.py
│   │   └── encryption.py           # Implementación de cifrado AES256
│   │
│   ├── storage/                    # Almacenamiento de datos
│   │   ├── __init__.py
│   │   └── vault.py                # Gestión del almacén de contraseñas
│   │
│   ├── ui/                          # Interfaz de usuario
│   │   ├── __init__.py
│   │   ├── login_window.py          # Ventana de inicio de sesión
│   │   ├── main_window.py           # Ventana principal
│   │   ├── password_entry_dialog.py # Diálogo para entrada de contraseñas
│   │   └── password_generator_dialog.py # Diálogo del generador de contraseñas
│   │
│   └── utils/                       # Utilidades
│       ├── __init__.py
│       ├── config.py                # Gestión de configuración
│       └── pyinstaller_utils.py     # Utilidades para PyInstaller
│
└── tests/                           # Pruebas unitarias y de integración
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

## Disclaimer / Aviso Legal

This software is provided "as is", without any express or implied warranties, including, but not limited to, the warranties of merchantability or fitness for a particular purpose. Fernando Aberto Velasquez Aguilera shall not be held liable for any damages or losses arising from the use or inability to use this software. Users assume full responsibility for testing and verifying the software's suitability for their intended purposes prior to deployment in any production environment. Use of this software is entirely at your own risk. For any commercial modifications or implementations, it is strongly recommended to seek independent legal counsel.

El software se distribuye "tal cual", sin garantías expresas o implícitas, incluyendo, entre otras, las garantías de comerciabilidad o idoneidad para un propósito específico. Fernando Aberto Velasquez Aguilera no se hace responsable de los daños o perjuicios derivados del uso o de la imposibilidad de uso del software. El usuario asume la responsabilidad completa de probar y verificar la idoneidad del software para los fines que pretenda, antes de emplearlo en entornos de producción. El uso del software es completamente bajo su propio riesgo. Se recomienda encarecidamente buscar asesoramiento legal independiente para cualquier modificación o implementación comercial.
