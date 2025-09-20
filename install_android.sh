#!/bin/bash

# Script de instalación automática para CHRISTIANX Android

echo "🚀 Instalando dependencias para CHRISTIANX Android..."

# Actualizar sistema
sudo apt update

# Instalar dependencias del sistema
echo "📦 Instalando dependencias del sistema..."
sudo apt install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# Instalar Python dependencies
echo "🐍 Instalando dependencias de Python..."
pip3 install --user buildozer cython

# Instalar Kivy
echo "📱 Instalando Kivy..."
pip3 install --user kivy[base]

# Crear directorios necesarios
echo "📁 Creando directorios..."
mkdir -p ~/.buildozer/android/platform/android-ndk-r25b
mkdir -p ~/.buildozer/android/platform/android-sdk

# Configurar variables de entorno
echo "🔧 Configurando variables de entorno..."
echo 'export ANDROID_HOME=~/.buildozer/android/platform/android-sdk' >> ~/.bashrc
echo 'export PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools' >> ~/.bashrc
echo 'export ANDROID_NDK_HOME=~/.buildozer/android/platform/android-ndk-r25b' >> ~/.bashrc

# Recargar bashrc
source ~/.bashrc

echo "✅ Instalación completada!"
echo ""
echo "📋 Próximos pasos:"
echo "1. Ejecuta: buildozer android debug"
echo "2. Espera a que se descarguen las dependencias de Android"
echo "3. El APK se generará en bin/christianx-1.0-debug.apk"
echo ""
echo "⚠️  Nota: La primera compilación puede tardar 30-60 minutos"
echo "   debido a la descarga de Android SDK y NDK"
