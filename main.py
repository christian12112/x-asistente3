#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CHRISTIANX - Asistente de Voz Inteligente para Android
Versión móvil optimizada
"""

import os
import sys
import time
import threading
import queue
import json
import pickle
import re
import math
import random
import subprocess
import webbrowser
import urllib.parse
import unicodedata
import difflib
import glob
import shutil
from datetime import datetime, timedelta
import pytz

# Kivy imports para Android
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.logger import Logger

# Imports condicionales para Android
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    Logger.warning("SpeechRecognition no disponible en Android")

try:
    from gtts import gTTS
    import pygame
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
    Logger.warning("gTTS no disponible en Android")

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    Logger.warning("Requests no disponible en Android")

class CHRISTIANXApp(App):
    def build(self):
        """Construir la interfaz de usuario"""
        self.title = "CHRISTIANX - Asistente de Voz"
        
        # Layout principal
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Título
        title = Label(
            text="CHRISTIANX - Asistente de Voz",
            size_hint_y=None,
            height=50,
            font_size=20,
            bold=True
        )
        main_layout.add_widget(title)
        
        # Área de chat
        self.chat_scroll = ScrollView()
        self.chat_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.chat_layout.bind(minimum_height=self.chat_layout.setter('height'))
        self.chat_scroll.add_widget(self.chat_layout)
        main_layout.add_widget(self.chat_scroll)
        
        # Input de texto
        self.text_input = TextInput(
            hint_text="Escribe tu comando aquí...",
            size_hint_y=None,
            height=40,
            multiline=False
        )
        self.text_input.bind(on_text_validate=self.on_enter_pressed)
        main_layout.add_widget(self.text_input)
        
        # Botones
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        
        self.send_button = Button(
            text="Enviar",
            size_hint_x=0.5
        )
        self.send_button.bind(on_press=self.send_message)
        
        self.voice_button = Button(
            text="🎤 Voz",
            size_hint_x=0.5
        )
        self.voice_button.bind(on_press=self.toggle_voice_listening)
        
        button_layout.add_widget(self.send_button)
        button_layout.add_widget(self.voice_button)
        main_layout.add_widget(button_layout)
        
        # Estado
        self.status_label = Label(
            text="Listo",
            size_hint_y=None,
            height=30,
            font_size=12
        )
        main_layout.add_widget(self.status_label)
        
        # Inicializar CHRISTIANX
        self.christianx = CHRISTIANX()
        self.is_listening = False
        
        return main_layout
    
    def on_enter_pressed(self, instance):
        """Manejar Enter en el input"""
        self.send_message()
    
    def send_message(self, instance=None):
        """Enviar mensaje"""
        message = self.text_input.text.strip()
        if message:
            self.add_message(f"Tú: {message}", "user")
            self.text_input.text = ""
            self.process_message(message)
    
    def toggle_voice_listening(self, instance):
        """Alternar escucha de voz"""
        if not SPEECH_RECOGNITION_AVAILABLE:
            self.add_message("❌ Reconocimiento de voz no disponible", "system")
            return
        
        if self.is_listening:
            self.stop_listening()
        else:
            self.start_listening()
    
    def start_listening(self):
        """Iniciar escucha de voz"""
        self.is_listening = True
        self.voice_button.text = "🛑 Parar"
        self.status_label.text = "Escuchando..."
        self.add_message("🎤 Escuchando...", "system")
        
        # Iniciar hilo de escucha
        threading.Thread(target=self.listen_voice, daemon=True).start()
    
    def stop_listening(self):
        """Parar escucha de voz"""
        self.is_listening = False
        self.voice_button.text = "🎤 Voz"
        self.status_label.text = "Listo"
        self.add_message("🛑 Escucha detenida", "system")
    
    def listen_voice(self):
        """Escuchar voz en hilo separado"""
        try:
            if not SPEECH_RECOGNITION_AVAILABLE:
                return
            
            r = sr.Recognizer()
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=1)
                audio = r.listen(source, timeout=5)
            
            text = r.recognize_google(audio, language='es-ES')
            Clock.schedule_once(lambda dt: self.process_voice_command(text))
            
        except sr.UnknownValueError:
            Clock.schedule_once(lambda dt: self.add_message("❌ No se pudo entender", "system"))
        except sr.RequestError as e:
            Clock.schedule_once(lambda dt: self.add_message(f"❌ Error: {e}", "system"))
        except Exception as e:
            Clock.schedule_once(lambda dt: self.add_message(f"❌ Error: {e}", "system"))
        finally:
            Clock.schedule_once(lambda dt: self.stop_listening())
    
    def process_voice_command(self, text):
        """Procesar comando de voz"""
        self.add_message(f"Escuché: {text}", "user")
        self.process_message(text)
    
    def process_message(self, message):
        """Procesar mensaje"""
        try:
            response = self.christianx.process_command(message)
            if response:
                self.add_message(f"CHRISTIANX: {response}", "assistant")
            else:
                self.add_message("CHRISTIANX: No entendí tu comando", "assistant")
        except Exception as e:
            self.add_message(f"❌ Error: {e}", "system")
    
    def add_message(self, text, sender="system"):
        """Agregar mensaje al chat"""
        color = {
            "user": (0.2, 0.6, 1, 1),
            "assistant": (0.2, 0.8, 0.2, 1),
            "system": (0.8, 0.8, 0.8, 1)
        }.get(sender, (0.8, 0.8, 0.8, 1))
        
        label = Label(
            text=text,
            text_size=(None, None),
            halign='left',
            valign='top',
            color=color,
            size_hint_y=None,
            height=40
        )
        self.chat_layout.add_widget(label)
        
        # Scroll hacia abajo
        Clock.schedule_once(lambda dt: self.scroll_to_bottom(), 0.1)
    
    def scroll_to_bottom(self):
        """Scroll hacia abajo"""
        self.chat_scroll.scroll_y = 0

class CHRISTIANX:
    """Versión simplificada de CHRISTIANX para Android"""
    
    def __init__(self):
        self.log_message("✅ CHRISTIANX iniciado en Android")
        self.recent_responses = []
        
    def log_message(self, message):
        """Log de mensajes"""
        Logger.info(f"CHRISTIANX: {message}")
    
    def process_command(self, command):
        """Procesar comando"""
        try:
            cmd_lower = command.lower().strip()
            
            # Comandos básicos
            if any(word in cmd_lower for word in ['hola', 'hi', 'hello']):
                return "¡Hola! Soy CHRISTIANX, tu asistente de voz. ¿En qué puedo ayudarte?"
            
            elif any(word in cmd_lower for word in ['hora', 'tiempo']):
                now = datetime.now()
                return f"Son las {now.strftime('%H:%M')} del {now.strftime('%d de %B de %Y')}"
            
            elif any(word in cmd_lower for word in ['ayuda', 'help', 'comandos']):
                return """Comandos disponibles:
                - Hola: Saludo
                - Hora: Hora actual
                - Ayuda: Mostrar esta ayuda
                - Buscar [término]: Buscar en internet
                - Música [canción]: Reproducir música"""
            
            elif 'buscar' in cmd_lower:
                search_term = cmd_lower.replace('buscar', '').strip()
                if search_term:
                    return f"Buscando información sobre: {search_term}"
                else:
                    return "¿Qué quieres que busque?"
            
            elif 'música' in cmd_lower or 'musica' in cmd_lower:
                song = cmd_lower.replace('música', '').replace('musica', '').strip()
                if song:
                    return f"Reproduciendo: {song}"
                else:
                    return "¿Qué música quieres escuchar?"
            
            elif any(word in cmd_lower for word in ['gracias', 'thanks']):
                return "¡De nada! Estoy aquí para ayudarte."
            
            elif any(word in cmd_lower for word in ['adiós', 'bye', 'chao']):
                return "¡Hasta luego! Fue un placer ayudarte."
            
            else:
                return "No entendí tu comando. Di 'ayuda' para ver los comandos disponibles."
                
        except Exception as e:
            self.log_message(f"Error procesando comando: {e}")
            return "Lo siento, ocurrió un error procesando tu comando."

if __name__ == "__main__":
    CHRISTIANXApp().run()
