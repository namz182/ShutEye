"""
Build script for ShutEye application using PyInstaller
Creates a standalone executable with all dependencies bundled
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path

# Configuration
APP_NAME = "ShutEye"
MAIN_SCRIPT = "main.py"
ICON_FILE = "assets/img/clock-logo.png"
BUILD_DIR = "build"
DIST_DIR = "dist"

def clean_build():
    """Remove previous build artifacts"""
    print("Cleaning previous builds...")
    for directory in [BUILD_DIR, DIST_DIR, "__pycache__"]:
        if os.path.exists(directory):
            shutil.rmtree(directory)
    
    spec_files = list(Path(".").glob("*.spec"))
    for spec_file in spec_files:
        os.remove(spec_file)
    
    print("Cleaned build directories")

def install_pyinstaller():
    """Install PyInstaller if not available"""
    try:
        import PyInstaller
        print("PyInstaller is already installed")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("PyInstaller installed")

def build_executable():
    """Build the executable using PyInstaller"""
    print(f"Building {APP_NAME}...")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--name", APP_NAME,
        "--onefile",  # Single executable file
        "--windowed",  # No console window
        "--clean",
        # Add data files
        "--add-data", "assets:assets",
        "--add-data", "config.json:.",
        "--add-data", "src:src",
        # Hidden imports
        "--hidden-import", "PIL",
        "--hidden-import", "PIL._tkinter_finder",
        "--hidden-import", "pystray",
        "--hidden-import", "customtkinter",
        # Icon
        f"--icon={ICON_FILE}" if os.path.exists(ICON_FILE) else "",
        # Main script
        MAIN_SCRIPT
    ]
    
    # Remove empty strings from command
    cmd = [c for c in cmd if c]
    
    try:
        subprocess.check_call(cmd)
        print(f"✅ Build successful! Executable created in {DIST_DIR}/")
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        sys.exit(1)

def create_spec_file():
    """Create a custom .spec file for more control"""
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['{MAIN_SCRIPT}'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets', 'assets'),
        ('config.json', '.'),
        ('src', 'src'),
    ],
    hiddenimports=[
        'PIL',
        'PIL._tkinter_finder',
        'pystray',
        'customtkinter',
        'tkinter',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{APP_NAME}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='{ICON_FILE}' if os.path.exists('{ICON_FILE}') else None,
)
'''
    
    spec_file = f"{APP_NAME}.spec"
    with open(spec_file, "w") as f:
        f.write(spec_content)
    
    print(f"✅ Created {spec_file}")
    return spec_file

def build_from_spec(spec_file):
    """Build using the spec file"""
    print(f"Building from {spec_file}...")
    
    try:
        subprocess.check_call(["pyinstaller", "--clean", spec_file])
        print(f"✅ Build successful! Executable in {DIST_DIR}/{APP_NAME}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        sys.exit(1)

def main():
    """Main build process"""
    print(f"🚀 Starting build process for {APP_NAME}")
    print("=" * 50)
    
    # Check if main script exists
    if not os.path.exists(MAIN_SCRIPT):
        print(f"❌ Error: {MAIN_SCRIPT} not found!")
        sys.exit(1)
    
    # Install PyInstaller
    install_pyinstaller()
    
    # Clean previous builds
    clean_build()
    
    # Create and build from spec file for better control
    spec_file = create_spec_file()
    build_from_spec(spec_file)
    
    print("=" * 50)
    print(f"✅ Build complete!")
    print(f"📁 Executable location: {DIST_DIR}/{APP_NAME}")
    print(f"💡 Run with: ./{DIST_DIR}/{APP_NAME}")

if __name__ == "__main__":
    main()
