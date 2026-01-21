# Building ShutEye Executable

## Quick Build

### Option 1: Using Python Script (Recommended)
```bash
python build.py
```
### Option 2: Manual PyInstaller
```bash
pip install pyinstaller
pyinstaller --name ShutEye --onefile --windowed --add-data "assets:assets" --add-data "config.json:." --add-data "src:src" main.py
```

## Build Output

After successful build:
- **Executable**: `dist/ShutEye` (Linux/Mac) or `dist/ShutEye.exe` (Windows)
- **Size**: ~50-100 MB (includes Python runtime and all dependencies)

## Running the Executable

```bash
./dist/ShutEye  # Linux/Mac
dist\ShutEye.exe  # Windows
```

## Build Requirements

- Python 3.8+
- PyInstaller (`pip install pyinstaller`)
- All project dependencies (see requirements.txt)