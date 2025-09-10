import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont
import pygame
import os
import time
import threading
from PIL import Image, ImageTk
import random

# Inicializar pygame mixer con mejor configuración
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)

class NodoCancion:
    def __init__(self, titulo, artista, duracion, genero="Desconocido", archivo_audio=None):
        self.titulo = titulo
        self.artista = artista
        self.duracion = duracion
        self.genero = genero
        self.archivo_audio = archivo_audio
        self.siguiente = None

    def __str__(self):
        return f"{self.titulo} - {self.artista} ({self.formatear_duracion()})"
    
    def formatear_duracion(self):
        minutos = self.duracion // 60
        segundos = self.duracion % 60
        return f"{minutos}:{segundos:02d}"

class Playlist:
    def __init__(self, nombre):
        self.nombre = nombre
        self.inicio = None
        self.actual = None
        self.tamaño = 0
        self.reproduciendo = False
        self.pausado = False
    
    def esta_vacia(self):
        return self.inicio is None
    
    def añadir_cancion(self, titulo, artista, duracion, genero="Desconocido", archivo_audio=None):
        nueva_cancion = NodoCancion(titulo, artista, duracion, genero, archivo_audio)
        
        if self.esta_vacia():
            self.inicio = nueva_cancion
            self.actual = nueva_cancion
        else:
            actual = self.inicio
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nueva_cancion
        
        self.tamaño += 1
        return nueva_cancion
    
    def eliminar_posicion(self, posicion):
        if self.esta_vacia():
            return False
        
        if posicion < 1 or posicion > self.tamaño:
            return False
        
        if posicion == 1:
            eliminada = self.inicio
            if self.actual == self.inicio:
                self.actual = self.inicio.siguiente if self.inicio.siguiente else None
            self.inicio = self.inicio.siguiente
            self.tamaño -= 1
            return eliminada
        
        anterior = self.inicio
        actual = self.inicio.siguiente
        contador = 2
        
        while actual is not None:
            if contador == posicion:
                if self.actual == actual:
                    self.actual = actual.siguiente if actual.siguiente else anterior
                anterior.siguiente = actual.siguiente
                self.tamaño -= 1
                return actual
            anterior = actual
            actual = actual.siguiente
            contador += 1
        
        return False
    
    def ordenar_por_titulo(self):
        if self.tamaño <= 1:
            return
        
        self.inicio = self._merge_sort(self.inicio, 'titulo')
        self.actual = self.inicio
    
    def ordenar_por_artista(self):
        if self.tamaño <= 1:
            return
        
        self.inicio = self._merge_sort(self.inicio, 'artista')
        self.actual = self.inicio
    
    def ordenar_por_duracion(self):
        if self.tamaño <= 1:
            return
        
        self.inicio = self._merge_sort(self.inicio, 'duracion')
        self.actual = self.inicio
    
    def _merge_sort(self, cabeza, criterio):
        if cabeza is None or cabeza.siguiente is None:
            return cabeza
        
        mitad = self._dividir_lista(cabeza)
        izquierda = cabeza
        derecha = mitad
        
        izquierda_ordenada = self._merge_sort(izquierda, criterio)
        derecha_ordenada = self._merge_sort(derecha, criterio)
        
        return self._fusionar(izquierda_ordenada, derecha_ordenada, criterio)
    
    def _dividir_lista(self, cabeza):
        if cabeza is None:
            return None
        
        tortuga = cabeza
        liebre = cabeza.siguiente
        
        while liebre is not None:
            liebre = liebre.siguiente
            if liebre is not None:
                tortuga = tortuga.siguiente
                liebre = liebre.siguiente
        
        mitad = tortuga.siguiente
        tortuga.siguiente = None
        return mitad
    
    def _fusionar(self, izquierda, derecha, criterio):
        dummy = NodoCancion("", "", 0)
        actual = dummy
        
        while izquierda is not None and derecha is not None:
            if criterio == 'titulo':
                condicion = izquierda.titulo.lower() <= derecha.titulo.lower()
            elif criterio == 'artista':
                condicion = izquierda.artista.lower() <= derecha.artista.lower()
            elif criterio == 'duracion':
                condicion = izquierda.duracion <= derecha.duracion
            else:
                condicion = True
            
            if condicion:
                actual.siguiente = izquierda
                izquierda = izquierda.siguiente
            else:
                actual.siguiente = derecha
                derecha = derecha.siguiente
            actual = actual.siguiente
        
        if izquierda is not None:
            actual.siguiente = izquierda
        elif derecha is not None:
            actual.siguiente = derecha
        
        return dummy.siguiente
    
    def obtener_lista(self):
        lista = []
        actual = self.inicio
        posicion = 1
        
        while actual is not None:
            lista.append({
                'posicion': posicion,
                'titulo': actual.titulo,
                'artista': actual.artista,
                'duracion': actual.formatear_duracion(),
                'genero': actual.genero,
                'es_actual': actual == self.actual,
                'nodo': actual
            })
            actual = actual.siguiente
            posicion += 1
        
        return lista
    
    def siguiente(self):
        if self.esta_vacia() or not self.actual:
            return False
        
        if self.actual.siguiente is not None:
            self.actual = self.actual.siguiente
        else:
            self.actual = self.inicio
        
        return self.actual
    
    def anterior(self):
        if self.esta_vacia() or not self.actual:
            return False
        
        if self.actual == self.inicio:
            actual = self.inicio
            while actual.siguiente is not None:
                actual = actual.siguiente
            self.actual = actual
        else:
            anterior = self.inicio
            while anterior.siguiente != self.actual:
                anterior = anterior.siguiente
            self.actual = anterior
        
        return self.actual
    
    def reproducir_audio(self):
        """Reproduce el audio de la canción actual COMPLETA"""
        if self.actual and self.actual.archivo_audio:
            try:
                # Verificar que el archivo existe y es MP3
                if not os.path.exists(self.actual.archivo_audio):
                    print(f"❌ Archivo no encontrado: {self.actual.archivo_audio}")
                    return False
                
                if not self.actual.archivo_audio.lower().endswith('.mp3'):
                    print(f"⚠️ Formato no MP3: {self.actual.archivo_audio}")
                    return False
                
                # Detener cualquier reproducción anterior
                pygame.mixer.music.stop()
                
                # Cargar y reproducir MP3 desde el inicio
                pygame.mixer.music.load(self.actual.archivo_audio)
                pygame.mixer.music.play()
                
                self.reproduciendo = True
                self.pausado = False
                
                print(f"✅ Reproduciendo: {self.actual.titulo} (completa)")
                return True
                
            except Exception as e:
                print(f"❌ Error reproduciendo audio: {e}")
                return False
        return False
    
    def pausar_audio(self):
        """Pausa la reproducción actual"""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.pausado = True
            self.reproduciendo = False
    
    def reanudar_audio(self):
        """Reanuda la reproducción pausada"""
        if self.pausado:
            pygame.mixer.music.unpause()
            self.pausado = False
            self.reproduciendo = True
    
    def detener_audio(self):
        """Detiene completamente la reproducción"""
        pygame.mixer.music.stop()
        self.reproduciendo = False
        self.pausado = False

class SpotifyStylePlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music player")
        self.root.geometry("1000x700")  # Ventana más pequeña sin barra de progreso
        self.root.configure(bg='#121212')
        self.root.minsize(900, 600)
        
        self.colors = {
            'bg_dark': '#121212',
            'bg_light': '#181818',
            'bg_lighter': '#282828',
            'green': '#1DB954',
            'white': '#FFFFFF',
            'gray': '#B3B3B3',
            'dark_gray': '#535353'
        }
        
        self.playlist = Playlist("Mi Playlist")
        self.setup_styles()
        self.setup_ui()
        self.cargar_canciones_ejemplo()
    
    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.style.configure('Dark.TFrame', background=self.colors['bg_dark'])
        self.style.configure('Light.TFrame', background=self.colors['bg_light'])
        self.style.configure('Lighter.TFrame', background=self.colors['bg_lighter'])
        
        self.style.configure('Title.TLabel', 
                           background=self.colors['bg_dark'],
                           foreground=self.colors['white'],
                           font=('Arial', 24, 'bold'))
        
        self.style.configure('Subtitle.TLabel',
                           background=self.colors['bg_dark'],
                           foreground=self.colors['gray'],
                           font=('Arial', 12))
        
        self.style.configure('Treeview',
                           background=self.colors['bg_light'],
                           foreground=self.colors['white'],
                           fieldbackground=self.colors['bg_light'],
                           borderwidth=0)
        
        self.style.configure('Treeview.Heading',
                           background=self.colors['bg_light'],
                           foreground=self.colors['gray'],
                           font=('Arial', 10, 'bold'),
                           borderwidth=0)
        
        self.style.map('Treeview',
                      background=[('selected', self.colors['dark_gray'])],
                      foreground=[('selected', self.colors['white'])])

    def setup_ui(self):
        main_container = ttk.Frame(self.root, style='Dark.TFrame', padding="0")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        sidebar = ttk.Frame(main_container, style='Dark.TFrame', width=200)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        sidebar.pack_propagate(False)
        
        ttk.Label(sidebar, text="🎵", font=('Arial', 24), 
                 background=self.colors['bg_dark'], foreground=self.colors['white']).pack(pady=20)
        ttk.Label(sidebar, text="MUSIC PLAYER", style='Subtitle.TLabel').pack()
        
        nav_options = ['Inicio', 'Buscar', 'Tu Biblioteca']
        for option in nav_options:
            btn = tk.Button(sidebar, text=option, font=('Arial', 12),
                          bg=self.colors['bg_dark'], fg=self.colors['gray'],
                          borderwidth=0, cursor='hand2')
            btn.pack(pady=10, anchor='w')
            btn.bind('<Enter>', lambda e, b=btn: b.config(fg=self.colors['white']))
            btn.bind('<Leave>', lambda e, b=btn: b.config(fg=self.colors['gray']))
        
        ttk.Label(sidebar, text="PLAYLISTS", style='Subtitle.TLabel').pack(pady=(30, 5), anchor='w')
        ttk.Label(sidebar, text="Mi Playlist", style='Subtitle.TLabel',
                 foreground=self.colors['white']).pack(anchor='w')
        
        content = ttk.Frame(main_container, style='Light.TFrame')
        content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 10), pady=10)
        
        header = tk.Canvas(content, bg=self.colors['bg_light'], height=120, highlightthickness=0)
        header.pack(fill=tk.X)
        
        for i in range(120):
            color = self.interpolate_color('#1DB954', '#121212', i/120)
            header.create_line(0, i, 1000, i, fill=color)
        
        header.create_text(20, 60, text="Mi Playlist", anchor='w',
                          fill='white', font=('Arial', 20, 'bold'))
        
        controls_frame = ttk.Frame(content, style='Light.TFrame')
        controls_frame.pack(fill=tk.X, pady=10)
        
        control_buttons = ttk.Frame(controls_frame, style='Light.TFrame')
        control_buttons.pack(pady=10)
        
        self.play_btn = tk.Button(control_buttons, text="▶", font=('Arial', 16, 'bold'),
                                bg=self.colors['green'], fg=self.colors['white'],
                                borderwidth=0, cursor='hand2', command=self.toggle_play,
                                width=3, height=1)
        self.play_btn.pack(side=tk.LEFT, padx=5)
        
        prev_btn = tk.Button(control_buttons, text="⏮", font=('Arial', 16),
                           bg=self.colors['bg_light'], fg=self.colors['white'],
                           borderwidth=0, cursor='hand2', command=self.anterior,
                           width=3, height=1)
        prev_btn.pack(side=tk.LEFT, padx=5)
        
        next_btn = tk.Button(control_buttons, text="⏭", font=('Arial', 16),
                           bg=self.colors['bg_light'], fg=self.colors['white'],
                           borderwidth=0, cursor='hand2', command=self.siguiente,
                           width=3, height=1)
        next_btn.pack(side=tk.LEFT, padx=5)
        
        # Botones de ordenamiento
        ordenamiento_frame = ttk.Frame(controls_frame, style='Light.TFrame')
        ordenamiento_frame.pack(pady=5)
        
        ttk.Label(ordenamiento_frame, text="Ordenar por:", 
                 style='Subtitle.TLabel', foreground=self.colors['white']).pack(side=tk.LEFT)
        
        tk.Button(ordenamiento_frame, text="Título", font=('Arial', 9),
                 bg=self.colors['bg_lighter'], fg=self.colors['white'],
                 command=self.ordenar_por_titulo, padx=5, pady=2).pack(side=tk.LEFT, padx=2)
        
        tk.Button(ordenamiento_frame, text="Artista", font=('Arial', 9),
                 bg=self.colors['bg_lighter'], fg=self.colors['white'],
                 command=self.ordenar_por_artista, padx=5, pady=2).pack(side=tk.LEFT, padx=2)
        
        tk.Button(ordenamiento_frame, text="Duración", font=('Arial', 9),
                 bg=self.colors['bg_lighter'], fg=self.colors['white'],
                 command=self.ordenar_por_duracion, padx=5, pady=2).pack(side=tk.LEFT, padx=2)
        
        # Botones de añadir/eliminar
        btn_frame = ttk.Frame(controls_frame, style='Light.TFrame')
        btn_frame.pack(pady=5)
        
        add_btn = tk.Button(btn_frame, text="➕ Añadir canción", font=('Arial', 10),
                          bg=self.colors['bg_lighter'], fg=self.colors['white'],
                          borderwidth=0, cursor='hand2', command=self.añadir_cancion,
                          padx=10, pady=5)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        self.remove_btn = tk.Button(btn_frame, text="🗑️ Eliminar", font=('Arial', 10),
                                  bg='#e74c3c', fg=self.colors['white'],
                                  borderwidth=0, cursor='hand2', command=self.eliminar_cancion,
                                  padx=10, pady=5)
        self.remove_btn.pack(side=tk.LEFT, padx=5)
        
        # Lista de canciones (más espacio sin la barra de progreso)
        list_container = ttk.Frame(content, style='Light.TFrame')
        list_container.pack(fill=tk.BOTH, expand=True, pady=10)
        
        tree_frame = ttk.Frame(list_container, style='Light.TFrame')
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('#', 'Título', 'Artista', 'Duración', 'Género')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor='center')
        
        self.tree.column('#', width=50)
        self.tree.column('Título', width=200, anchor='w')
        self.tree.column('Artista', width=150, anchor='w')
        self.tree.column('Duración', width=80)
        self.tree.column('Género', width=120)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Barra inferior de información (sin controles de progreso)
        now_playing = ttk.Frame(content, style='Lighter.TFrame', height=60)
        now_playing.pack(fill=tk.X, side=tk.BOTTOM)
        now_playing.pack_propagate(False)
        
        self.now_playing_text = tk.StringVar()
        self.now_playing_text.set("Selecciona una canción para reproducir")
        
        now_playing_label = ttk.Label(now_playing, textvariable=self.now_playing_text,
                                     style='Subtitle.TLabel', foreground=self.colors['white'])
        now_playing_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Solo control de volumen
        audio_controls = ttk.Frame(now_playing, style='Lighter.TFrame')
        audio_controls.pack(side=tk.RIGHT, padx=20)
        
        ttk.Label(audio_controls, text="Volumen:", 
                 style='Subtitle.TLabel', foreground=self.colors['white']).pack(side=tk.LEFT, padx=5)
        
        self.volumen_scale = tk.Scale(audio_controls, from_=0, to=100, orient=tk.HORIZONTAL,
                                    bg=self.colors['bg_lighter'], fg=self.colors['white'],
                                    troughcolor=self.colors['dark_gray'],
                                    sliderlength=10, length=80,
                                    command=self.ajustar_volumen)
        self.volumen_scale.set(70)
        self.volumen_scale.pack(side=tk.LEFT, padx=5)
        
        self.tree.bind('<Double-1>', self.on_double_click)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
    
    def interpolate_color(self, color1, color2, ratio):
        r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
        r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
        
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def cargar_canciones_ejemplo(self):
        canciones = [
            ("When I Come Around", "GreenDay", 178, "punk", "C:/Users/HP/Documents/trabajo de competencias EstructuraDatos/Playlist-musica/Music-Player/audio/when_i_come_around.mp3"),
            ("Given Up", "Linkin Park", 189, "metal", "C:/Users/HP/Documents/trabajo de competencias EstructuraDatos/Playlist-musica/Music-Player/audio/given_up.mp3"),
            ("Not Today", "Twenty One Pilots", 238, "Alternativa", "C:/Users/HP/Documents/trabajo de competencias EstructuraDatos/Playlist-musica/Music-Player/audio/not_today.mp3"),
            ("Smells Like Teen Spirit (Live)", "Rockin'1000", 307, "Rock", "C:/Users/HP/Documents/trabajo de competencias EstructuraDatos/Playlist-musica/Music-Player/audio/SmellsLikeTeenSpirit.mp3"),
            ("Karma Police", "Radiohead", 264, "Alternativa", "C:/Users/HP/Documents/trabajo de competencias EstructuraDatos/Playlist-musica/Music-Player/audio/karma_police.mp3"),
            ("MLP Theme Song", "MLP", 35, "Pop", "C:/Users/HP/Documents/trabajo de competencias EstructuraDatos/Playlist-musica/Music-Player/audio/mlp.mp3"),
            ("Symphony", "Clean Bandit", 213, "Pop", "C:/Users/HP/Documents/trabajo de competencias EstructuraDatos/Playlist-musica/Music-Player/audio/symphony.mp3"),
        ]
        
        for titulo, artista, duracion, genero, archivo in canciones:
            if archivo and os.path.exists(archivo) and archivo.lower().endswith('.mp3'):
                print(f"✅ Añadiendo: {titulo} - {archivo}")
                self.playlist.añadir_cancion(titulo, artista, duracion, genero, archivo)
            else:
                print(f"⚠️  Archivo no encontrado o no es MP3: {archivo}")
                # Añadir sin audio pero con la duración correcta
                self.playlist.añadir_cancion(titulo, artista, duracion, genero, None)
        
        self.actualizar_lista()
    
    def actualizar_lista(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for cancion in self.playlist.obtener_lista():
            valores = (
                cancion['posicion'],
                cancion['titulo'],
                cancion['artista'],
                cancion['duracion'],
                cancion['genero']
            )
            item = self.tree.insert('', tk.END, values=valores, tags=('cancion',))
            
            if cancion['es_actual']:
                self.tree.selection_set(item)
                self.tree.focus(item)
                self.actualizar_info_cancion(cancion['nodo'])
    
    def actualizar_info_cancion(self, cancion):
        if cancion:
            info = f"🎵 {cancion.titulo} - {cancion.artista}"
            if cancion.archivo_audio:
                info += " 🔊"  # Indicador de audio real
            self.now_playing_text.set(info)
        else:
            self.now_playing_text.set("Selecciona una canción para reproducir")
    
    def toggle_play(self):
        if self.playlist.esta_vacia():
            messagebox.showinfo("Info", "No hay canciones en la playlist")
            return
        
        if self.playlist.pausado:
            self.playlist.reanudar_audio()
            self.play_btn.config(text="⏸")
        elif self.playlist.reproduciendo:
            self.playlist.pausar_audio()
            self.play_btn.config(text="▶")
        else:
            if self.playlist.actual and self.playlist.actual.archivo_audio:
                if self.playlist.reproducir_audio():
                    self.play_btn.config(text="⏸")
                else:
                    messagebox.showinfo("Info", "Error al reproducir el archivo de audio")
            else:
                messagebox.showinfo("Info", "No hay archivo de audio para esta canción")
    
    def siguiente(self):
        if self.playlist.siguiente():
            self.playlist.detener_audio()
            if self.playlist.actual and self.playlist.actual.archivo_audio:
                if self.playlist.reproducir_audio():
                    self.play_btn.config(text="⏸")
            self.actualizar_lista()
    
    def anterior(self):
        if self.playlist.anterior():
            self.playlist.detener_audio()
            if self.playlist.actual and self.playlist.actual.archivo_audio:
                if self.playlist.reproducir_audio():
                    self.play_btn.config(text="⏸")
            self.actualizar_lista()
    
    def ajustar_volumen(self, value):
        volumen = float(value) / 100.0
        pygame.mixer.music.set_volume(volumen)
    
    def ordenar_por_titulo(self):
        self.playlist.ordenar_por_titulo()
        self.actualizar_lista()
        messagebox.showinfo("Ordenado", "Playlist ordenada por título")
    
    def ordenar_por_artista(self):
        self.playlist.ordenar_por_artista()
        self.actualizar_lista()
        messagebox.showinfo("Ordenado", "Playlist ordenada por artista")
    
    def ordenar_por_duracion(self):
        self.playlist.ordenar_por_duracion()
        self.actualizar_lista()
        messagebox.showinfo("Ordenado", "Playlist ordenada por duración")
    
    def on_double_click(self, event):
        self.reproducir_seleccionada()
    
    def on_select(self, event):
        pass
    
    def reproducir_seleccionada(self):
        seleccion = self.tree.selection()
        if not seleccion:
            return
        
        item = seleccion[0]
        valores = self.tree.item(item, 'values')
        posicion = int(valores[0])
        
        actual = self.playlist.inicio
        for i in range(1, posicion):
            actual = actual.siguiente
        
        self.playlist.actual = actual
        self.playlist.detener_audio()
        if self.playlist.actual.archivo_audio:
            if self.playlist.reproducir_audio():
                self.play_btn.config(text="⏸")
        self.actualizar_lista()
    
    def añadir_cancion(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Añadir Canción")
        dialog.geometry("400x350")
        dialog.configure(bg=self.colors['bg_light'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Título:", bg=self.colors['bg_light'], fg='white').grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        titulo_entry = tk.Entry(dialog, bg=self.colors['bg_lighter'], fg='white', insertbackground='white')
        titulo_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Artista:", bg=self.colors['bg_light'], fg='white').grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        artista_entry = tk.Entry(dialog, bg=self.colors['bg_lighter'], fg='white', insertbackground='white')
        artista_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Duración (segundos):", bg=self.colors['bg_light'], fg='white').grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        duracion_entry = tk.Entry(dialog, bg=self.colors['bg_lighter'], fg='white', insertbackground='white')
        duracion_entry.grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Género:", bg=self.colors['bg_light'], fg='white').grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        genero_entry = tk.Entry(dialog, bg=self.colors['bg_lighter'], fg='white', insertbackground='white')
        genero_entry.grid(row=3, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Archivo MP3:", bg=self.colors['bg_light'], fg='white').grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
        audio_entry = tk.Entry(dialog, bg=self.colors['bg_lighter'], fg='white', insertbackground='white')
        audio_entry.grid(row=4, column=1, padx=10, pady=5)
        
        def guardar():
            try:
                titulo = titulo_entry.get()
                artista = artista_entry.get()
                duracion = int(duracion_entry.get())
                genero = genero_entry.get() or "Desconocido"
                archivo_audio = audio_entry.get() or None
                
                if archivo_audio and not archivo_audio.lower().endswith('.mp3'):
                    messagebox.showwarning("Formato incorrecto", "Solo se soportan archivos MP3")
                    return
                
                if archivo_audio and not os.path.exists(archivo_audio):
                    messagebox.showwarning("Archivo no encontrado", "El archivo MP3 no existe")
                    return
                
                if titulo and artista and duracion > 0:
                    self.playlist.añadir_cancion(titulo, artista, duracion, genero, archivo_audio)
                    self.actualizar_lista()
                    dialog.destroy()
                    messagebox.showinfo("Éxito", "Canción añadida correctamente")
                else:
                    messagebox.showerror("Error", "Por favor completa todos los campos")
            except ValueError:
                messagebox.showerror("Error", "La duración debe ser un número")
        
        tk.Button(dialog, text="Añadir", bg=self.colors['green'], fg='white',
                 command=guardar).grid(row=5, column=1, pady=20)
        tk.Button(dialog, text="Cancelar", bg=self.colors['dark_gray'], fg='white',
                 command=dialog.destroy).grid(row=5, column=0, pady=20)
    
    def eliminar_cancion(self):
        if self.playlist.esta_vacia():
            messagebox.showinfo("Info", "La playlist está vacía")
            return
        
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showinfo("Info", "Selecciona una canción para eliminar")
            return
        
        item = seleccion[0]
        valores = self.tree.item(item, 'values')
        posicion = int(valores[0])
        titulo = valores[1]
        
        if messagebox.askyesno("Confirmar eliminación", 
                              f"¿Estás seguro de que quieres eliminar:\n\"{titulo}\"?"):
            cancion_eliminada = self.playlist.eliminar_posicion(posicion)
            
            if cancion_eliminada:
                if self.playlist.actual == cancion_eliminada:
                    self.playlist.detener_audio()
                    if self.playlist.inicio:
                        self.playlist.actual = self.playlist.inicio
                    else:
                        self.playlist.actual = None
                    self.play_btn.config(text="▶")
                
                self.actualizar_lista()
                messagebox.showinfo("Eliminada", f"\"{titulo}\" ha sido eliminada de la playlist")
            else:
                messagebox.showerror("Error", "No se pudo eliminar la canción")

def main():
    root = tk.Tk()
    app = SpotifyStylePlayer(root)
    root.mainloop()

if __name__ == "__main__":
    main()