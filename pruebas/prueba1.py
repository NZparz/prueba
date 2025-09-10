class NodoCancion:
    def __init__(self, titulo, artista, duracion):
        self.titulo = titulo
        self.artista = artista
        self.duracion = duracion  # en segundos
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
    
    def esta_vacia(self):
        return self.inicio is None
    
    def añadir_cancion(self, titulo, artista, duracion):
        nueva_cancion = NodoCancion(titulo, artista, duracion)
        
        if self.esta_vacia():
            self.inicio = nueva_cancion
            self.actual = nueva_cancion
        else:
            actual = self.inicio
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nueva_cancion
        
        self.tamaño += 1
        print(f"✓ '{titulo}' añadida a la playlist")
    
    def añadir_cancion_posicion(self, titulo, artista, duracion, posicion):
        if posicion < 1 or posicion > self.tamaño + 1:
            print("❌ Posición inválida")
            return False
        
        nueva_cancion = NodoCancion(titulo, artista, duracion)
        
        if posicion == 1:  # Al inicio
            nueva_cancion.siguiente = self.inicio
            self.inicio = nueva_cancion
            if self.actual is None:
                self.actual = nueva_cancion
        else:
            actual = self.inicio
            for _ in range(posicion - 2):
                actual = actual.siguiente
            nueva_cancion.siguiente = actual.siguiente
            actual.siguiente = nueva_cancion
        
        self.tamaño += 1
        print(f"✓ '{titulo}' añadida en posición {posicion}")
        return True
    
    def eliminar_cancion(self, titulo):
        if self.esta_vacia():
            print("❌ La playlist está vacía")
            return False
        
        # Caso especial: eliminar la primera canción
        if self.inicio.titulo.lower() == titulo.lower():
            if self.actual == self.inicio:
                self.actual = self.inicio.siguiente if self.inicio.siguiente else self.inicio
            eliminada = self.inicio
            self.inicio = self.inicio.siguiente
            self.tamaño -= 1
            print(f"✓ '{eliminada.titulo}' eliminada de la playlist")
            return True
        
        # Buscar la canción a eliminar
        anterior = self.inicio
        actual = self.inicio.siguiente
        
        while actual is not None:
            if actual.titulo.lower() == titulo.lower():
                if self.actual == actual:
                    self.actual = actual.siguiente if actual.siguiente else self.inicio
                anterior.siguiente = actual.siguiente
                self.tamaño -= 1
                print(f"✓ '{actual.titulo}' eliminada de la playlist")
                return True
            anterior = actual
            actual = actual.siguiente
        
        print(f"❌ Canción '{titulo}' no encontrada")
        return False
    
    def eliminar_posicion(self, posicion):
        if self.esta_vacia():
            print(" La playlist está vacía")
            return False
        
        if posicion < 1 or posicion > self.tamaño:
            print(" Posición inválida")
            return False
        
        if posicion == 1:
            if self.actual == self.inicio:
                self.actual = self.inicio.siguiente if self.inicio.siguiente else self.inicio
            eliminada = self.inicio
            self.inicio = self.inicio.siguiente
            self.tamaño -= 1
            print(f"✓ '{eliminada.titulo}' eliminada de la posición {posicion}")
            return True
        
        anterior = self.inicio
        actual = self.inicio.siguiente
        contador = 2
        
        while actual is not None:
            if contador == posicion:
                if self.actual == actual:
                    self.actual = actual.siguiente if actual.siguiente else self.inicio
                anterior.siguiente = actual.siguiente
                self.tamaño -= 1
                print(f"✓ '{actual.titulo}' eliminada de la posición {posicion}")
                return True
            anterior = actual
            actual = actual.siguiente
            contador += 1
        
        return False
    
    def reproducir_actual(self):
        if self.esta_vacia():
            print("No hay canciones en la playlist")
            return
        
        print(f"Reproduciendo: {self.actual}")
    
    def siguiente(self):
        if self.esta_vacia():
            print("No hay canciones en la playlist")
            return
        
        if self.actual.siguiente is not None:
            self.actual = self.actual.siguiente
        else:
            self.actual = self.inicio  # Volver al inicio
        
        print("Siguiente canción:")
        self.reproducir_actual()
    
    def anterior(self):
        if self.esta_vaza():
            print("No hay canciones en la playlist")
            return
        
        # En lista simple, debemos recorrer desde el inicio
        if self.actual == self.inicio:
            # Si es la primera, ir a la última
            actual = self.inicio
            while actual.siguiente is not None:
                actual = actual.siguiente
            self.actual = actual
        else:
            # Buscar el nodo anterior al actual
            anterior = self.inicio
            while anterior.siguiente != self.actual:
                anterior = anterior.siguiente
            self.actual = anterior
        
        print(" Canción anterior:")
        self.reproducir_actual()
    
    def buscar_cancion(self, titulo):
        actual = self.inicio
        posicion = 1
        
        while actual is not None:
            if actual.titulo.lower() == titulo.lower():
                print(f" Encontrada en posición {posicion}: {actual}")
                return actual, posicion
            actual = actual.siguiente
            posicion += 1
        
        print(f" Canción '{titulo}' no encontrada")
        return None, -1
    
    def mostrar_playlist(self):
        if self.esta_vacia():
            print(" La playlist está vacía")
            return
        
        print(f"\n🎶 PLAYLIST: {self.nombre} ({self.tamaño} canciones)")
        print("=" * 60)
        
        actual = self.inicio
        posicion = 1
        
        while actual is not None:
            indicador = "▶ " if actual == self.actual else "  "
            print(f"{indicador}{posicion:2d}. {actual}")
            actual = actual.siguiente
            posicion += 1
        print("=" * 60)
        print(f"  Duración total: {self.duracion_total()}\n")
    
    def duracion_total(self):
        total = 0
        actual = self.inicio
        
        while actual is not None:
            total += actual.duracion
            actual = actual.siguiente
        
        minutos = total // 60
        segundos = total % 60
        horas = minutos // 60
        minutos = minutos % 60
        
        if horas > 0:
            return f"{horas}h {minutos:02d}m {segundos:02d}s"
        else:
            return f"{minutos:02d}m {segundos:02d}s"

def mostrar_menu():
    print("\n" + "=" * 50)
    print(" MENÚ PLAYLIST MUSICAL")
    print("=" * 50)
    print("1. Mostrar playlist")
    print("2. Añadir canción al final")
    print("3.  Añadir canción en posición específica")
    print("4. Eliminar canción por título")
    print("5.  Eliminar canción por posición")
    print("6. Buscar canción")
    print("7.  Reproducir canción actual")
    print("8  Siguiente canción")
    print("9.   Canción anterior")
    print("10. Mostrar duración total")
    print("11. Salir")
    print("=" * 50)

def main():
    # Crear playlist inicial con algunas canciones
    playlist = Playlist("Mi Playlist Personal")
    
    # Canciones de ejemplo
    canciones_ejemplo = [
        ("Bohemian Rhapsody", "Queen", 355),
        ("Hotel California", "Eagles", 391),
        ("Imagine", "John Lennon", 183)
    ]
    
    for titulo, artista, duracion in canciones_ejemplo:
        playlist.añadir_cancion(titulo, artista, duracion)
    
    while True:
        mostrar_menu()
        try:
            opcion = int(input("\nSelecciona una opción (1-11): "))
            
            if opcion == 1:
                playlist.mostrar_playlist()
                
            elif opcion == 2:
                print("\nAñadir nueva canción:")
                titulo = input("Título: ")
                artista = input("Artista: ")
                try:
                    duracion = int(input("Duración en segundos: "))
                    playlist.añadir_cancion(titulo, artista, duracion)
                except ValueError:
                    print("La duración debe ser un número")
                    
            elif opcion == 3:
                print("\nAñadir canción en posición específica:")
                titulo = input("Título: ")
                artista = input("Artista: ")
                try:
                    duracion = int(input("Duración en segundos: "))
                    posicion = int(input("Posición: "))
                    playlist.añadir_cancion_posicion(titulo, artista, duracion, posicion)
                except ValueError:
                    print("La duración y posición deben ser números")
                    
            elif opcion == 4:
                print("\nEliminar canción por título:")
                titulo = input("Título de la canción a eliminar: ")
                playlist.eliminar_cancion(titulo)
                
            elif opcion == 5:
                print("\nEliminar canción por posición:")
                try:
                    posicion = int(input("Número de posición a eliminar: "))
                    playlist.eliminar_posicion(posicion)
                except ValueError:
                    print("La posición debe ser un número")
                    
            elif opcion == 6:
                print("\nBuscar canción:")
                titulo = input("Título de la canción a buscar: ")
                playlist.buscar_cancion(titulo)
                
            elif opcion == 7:
                print("\nReproduciendo:")
                playlist.reproducir_actual()
                
            elif opcion == 8:
                playlist.siguiente()
                
            elif opcion == 9:
                playlist.anterior()
                
            elif opcion == 10:
                print(f"\nDuración total: {playlist.duracion_total()}")
                
            elif opcion == 11:
                print("🎶 ¡Gracias por usar el reproductor musical! ")
                break
                
            else:
                print("Opción inválida. Por favor elige 1-11.")
                
            # Pausa para ver resultados
            input("\nPresiona Enter para continuar...")
            
        except ValueError:
            print("Por favor ingresa un número válido")
        except KeyboardInterrupt:
            print("\n\nPrograma interrumpido. ¡Hasta luego! ")
            break

if __name__ == "__main__":
    main()