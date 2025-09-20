# CHRISTIANX - APK para Android

## Instrucciones para crear el APK

### 1. Instalar dependencias

```bash
# Instalar Buildozer
pip install buildozer

# Instalar Cython
pip install cython

# Instalar dependencias del sistema (Ubuntu/Debian)
sudo apt update
sudo apt install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
```

### 2. Configurar Android SDK

```bash
# Crear directorio para Android SDK
mkdir -p ~/.buildozer/android/platform/android-ndk-r25b
mkdir -p ~/.buildozer/android/platform/android-sdk

# Descargar Android SDK
wget https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip
unzip commandlinetools-linux-9477386_latest.zip -d ~/.buildozer/android/platform/android-sdk/
```

### 3. Compilar APK

```bash
# Compilar APK
buildozer android debug

# O para release
buildozer android release
```

### 4. Archivos generados

- `bin/christianx-1.0-debug.apk` - APK de debug
- `bin/christianx-1.0-release.apk` - APK de release

## Características de la versión Android

### ✅ Funcionalidades incluidas:
- Interfaz gráfica con Kivy
- Reconocimiento de voz (si está disponible)
- Comandos básicos de voz
- Chat por texto
- Respuestas inteligentes

### ⚠️ Limitaciones en Android:
- Algunas librerías pueden no estar disponibles
- Funcionalidades de escritorio no funcionan
- Acceso limitado al sistema

### 📱 Permisos requeridos:
- INTERNET: Para búsquedas web
- RECORD_AUDIO: Para reconocimiento de voz
- WRITE_EXTERNAL_STORAGE: Para guardar archivos
- READ_EXTERNAL_STORAGE: Para leer archivos

## Solución de problemas

### Error: "No module named 'kivy'"
```bash
pip install kivy[base]
```

### Error: "Android SDK not found"
```bash
export ANDROID_HOME=~/.buildozer/android/platform/android-sdk
export PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools
```

### Error: "NDK not found"
```bash
export ANDROID_NDK_HOME=~/.buildozer/android/platform/android-ndk-r25b
```

## Personalización

### Cambiar icono:
1. Reemplazar `icon.png` con tu icono (48x48 px)
2. Recompilar: `buildozer android debug`

### Cambiar nombre de la app:
1. Editar `buildozer.spec`
2. Cambiar `title` y `package.name`
3. Recompilar

### Agregar más funcionalidades:
1. Editar `main.py`
2. Agregar nuevos comandos en `process_command()`
3. Recompilar
