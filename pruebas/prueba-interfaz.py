import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import time
from PIL import Image, ImageTk
import os

class NodoCancion:
    def __init__(self, titulo, artista, duracion, genero="Desconocido"):
        self.titulo = titulo
        self.artista = artista
        self.duracion = duracion
        self.genero = genero
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
    
    def esta_vacia(self):
        return self.inicio is None
    
    def añadir_cancion(self, titulo, artista, duracion, genero="Desconocido"):
        nueva_cancion = NodoCancion(titulo, artista, duracion, genero)
        
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
                self.actual = self.inicio.siguiente if self.inicio.siguiente else self.inicio
            self.inicio = self.inicio.siguiente
            self.tamaño -= 1
            return eliminada
        
        anterior = self.inicio
        actual = self.inicio.siguiente
        contador = 2
        
        while actual is not None:
            if contador == posicion:
                if self.actual == actual:
                    self.actual = actual.siguiente if actual.siguiente else self.inicio
                anterior.siguiente = actual.siguiente
                self.tamaño -= 1
                return actual
            anterior = actual
            actual = actual.siguiente
            contador += 1
        
        return False
    
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
        if self.esta_vacia():
            return False
        
        if self.actual.siguiente is not None:
            self.actual = self.actual.siguiente
        else:
            self.actual = self.inicio
        
        return self.actual
    
    def anterior(self):
        if self.esta_vacia():
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

class ReproductorMusical:
    def __init__(self, root):
        self.root = root
        self.root.title("🎵 Reproductor Musical")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        self.playlist = Playlist("Mi Música")
        self.setup_ui()
        self.cargar_canciones_ejemplo()
    
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Header con título
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(header_frame, text="🎵 REPRODUCTOR MUSICAL", 
                 font=('Arial', 16, 'bold'), foreground='#3498db').pack()
        
        ttk.Label(header_frame, text=self.playlist.nombre, 
                 font=('Arial', 12), foreground='#7f8c8d').pack()
        
        # Controles de reproducción
        controls_frame = ttk.Frame(main_frame)
        controls_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=10)
        
        # Botones de control
        btn_style = ttk.Style()
        btn_style.configure('Control.TButton', font=('Arial', 10))
        
        ttk.Button(controls_frame, text="⏮️ Anterior", 
                  command=self.anterior, style='Control.TButton').pack(side=tk.LEFT, padx=5)
        
        self.btn_play = ttk.Button(controls_frame, text="▶ Reproducir", 
                                  command=self.toggle_play, style='Control.TButton')
        self.btn_play.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(controls_frame, text="⏭️ Siguiente", 
                  command=self.siguiente, style='Control.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(controls_frame, text="➕ Añadir", 
                  command=self.añadir_cancion, style='Control.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(controls_frame, text="🗑️ Eliminar", 
                  command=self.eliminar_cancion, style='Control.TButton').pack(side=tk.LEFT, padx=5)
        
        # Información de la canción actual
        info_frame = ttk.LabelFrame(main_frame, text="Canción Actual", padding="10")
        info_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=10)
        
        self.info_text = tk.StringVar()
        self.info_text.set("Selecciona una canción para reproducir")
        
        ttk.Label(info_frame, textvariable=self.info_text, 
                 font=('Arial', 11), wraplength=400).pack()
        
        # Lista de canciones
        list_frame = ttk.LabelFrame(main_frame, text="Playlist", padding="10")
        list_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Treeview para mostrar la playlist
        columns = ('#', 'Título', 'Artista', 'Duración', 'Género')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        self.tree.column('#', width=50)
        self.tree.column('Título', width=150)
        self.tree.column('Artista', width=120)
        self.tree.column('Duración', width=80)
        self.tree.column('Género', width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configurar pesos
        list_frame.rowconfigure(0, weight=1)
        list_frame.columnconfigure(0, weight=1)
        
        # Bind double click
        self.tree.bind('<Double-1>', self.on_double_click)
    
    def cargar_canciones_ejemplo(self):
        canciones = [
            ("Bohemian Rhapsody", "Queen", 355, "Rock"),
            ("Hotel California", "Eagles", 391, "Rock"),
            ("Imagine", "John Lennon", 183, "Pop"),
            ("Sweet Child O' Mine", "Guns N' Roses", 356, "Rock"),
            ("Billie Jean", "Michael Jackson", 294, "Pop"),
            ("Smells Like Teen Spirit", "Nirvana", 301, "Grunge")
        ]
        
        for titulo, artista, duracion, genero in canciones:
            self.playlist.añadir_cancion(titulo, artista, duracion, genero)
        
        self.actualizar_lista()
    
    def actualizar_lista(self):
        # Limpiar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Agregar canciones
        for cancion in self.playlist.obtener_lista():
            valores = (
                cancion['posicion'],
                cancion['titulo'],
                cancion['artista'],
                cancion['duracion'],
                cancion['genero']
            )
            item = self.tree.insert('', tk.END, values=valores)
            
            if cancion['es_actual']:
                self.tree.selection_set(item)
                self.tree.focus(item)
                self.actualizar_info_cancion(cancion['nodo'])
    
    def actualizar_info_cancion(self, cancion):
        if cancion:
            info = f"🎵 {cancion.titulo} - {cancion.artista}\n"
            info += f"⏱️ Duración: {cancion.formatear_duracion()} | 🎶 Género: {cancion.genero}"
            self.info_text.set(info)
        else:
            self.info_text.set("Selecciona una canción para reproducir")
    
    def toggle_play(self):
        if self.playlist.esta_vaza():
            messagebox.showinfo("Info", "No hay canciones en la playlist")
            return
        
        self.playlist.reproduciendo = not self.playlist.reproduciendo
        if self.playlist.reproduciendo:
            self.btn_play.config(text="⏸️ Pausar")
            # Simular reproducción (en app real aquí iría el reproductor)
        else:
            self.btn_play.config(text="▶ Reproducir")
    
    def siguiente(self):
        if self.playlist.siguiente():
            self.actualizar_lista()
            self.playlist.reproduciendo = True
            self.btn_play.config(text="⏸️ Pausar")
    
    def anterior(self):
        if self.playlist.anterior():
            self.actualizar_lista()
            self.playlist.reproduciendo = True
            self.btn_play.config(text="⏸️ Pausar")
    
    def on_double_click(self, event):
        item = self.tree.selection()[0]
        valores = self.tree.item(item, 'values')
        posicion = int(valores[0])
        
        # Buscar la canción y establecer como actual
        actual = self.playlist.inicio
        for i in range(1, posicion):
            actual = actual.siguiente
        
        self.playlist.actual = actual
        self.actualizar_lista()
        self.playlist.reproduciendo = True
        self.btn_play.config(text="⏸️ Pausar")
    
    def añadir_cancion(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Añadir Canción")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Título:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        titulo_entry = ttk.Entry(dialog, width=30)
        titulo_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Artista:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        artista_entry = ttk.Entry(dialog, width=30)
        artista_entry.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Duración (segundos):").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        duracion_entry = ttk.Entry(dialog, width=30)
        duracion_entry.grid(row=2, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Género:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        genero_entry = ttk.Entry(dialog, width=30)
        genero_entry.grid(row=3, column=1, padx=10, pady=5)
        
        def guardar():
            try:
                titulo = titulo_entry.get()
                artista = artista_entry.get()
                duracion = int(duracion_entry.get())
                genero = genero_entry.get() or "Desconocido"
                
                if titulo and artista and duracion > 0:
                    self.playlist.añadir_cancion(titulo, artista, duracion, genero)
                    self.actualizar_lista()
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Por favor completa todos los campos correctamente")
            except ValueError:
                messagebox.showerror("Error", "La duración debe ser un número")
        
        ttk.Button(dialog, text="Añadir", command=guardar).grid(row=4, column=1, pady=20)
        ttk.Button(dialog, text="Cancelar", command=dialog.destroy).grid(row=4, column=0, pady=20)
    
    def eliminar_cancion(self):
        if self.playlist.esta_vaza():
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
        
        if messagebox.askyesno("Confirmar", f"¿Eliminar '{titulo}'?"):
            if self.playlist.eliminar_posicion(posicion):
                self.actualizar_lista()
                messagebox.showinfo("Éxito", f"Canción '{titulo}' eliminada")

def main():
    root = tk.Tk()
    app = ReproductorMusical(root)
    root.mainloop()

if __name__ == "__main__":
    main()