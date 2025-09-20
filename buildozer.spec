[app]

# (str) Título de la aplicación
title = CHRISTIANX

# (str) Nombre del paquete
package.name = christianx

# (str) Dominio del paquete
package.domain = com.christianx

# (str) Código fuente donde está main.py
source.dir = .

# (list) Archivos fuente a incluir
source.include_exts = py,png,jpg,kv,atlas

# (str) Archivo principal
source.main = main.py

# (str) Versión de la aplicación
version = 1.0

# (list) Requisitos de la aplicación
requirements = python3,kivy,pyjnius,android,plyer,requests,speechrecognition,gtts,pygame

# (str) Orientación permitida
orientation = portrait

# (bool) Indicar si la aplicación es fullscreen
fullscreen = 0

# (str) Versión de Android
android.minapi = 21

# (str) Versión de Android target
android.api = 30

# (str) NDK version
android.ndk = 25b

# (bool) Usar private storage
android.private_storage = True

# (str) Permisos de Android
android.permissions = INTERNET,RECORD_AUDIO,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (str) Características de Android
android.features = android.hardware.microphone

# (list) Archivos a incluir en el APK
android.include_exts = py,png,jpg,kv,atlas

# (str) Icono de la aplicación
icon.filename = icon.png

# (str) Logo de la aplicación
logo.filename = logo.png
