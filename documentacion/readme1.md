# Estructura de lista simple con nodos:
## 1. Clase NodoCancion (Cada canción es un nodo)
```
python
class NodoCancion:
    def __init__(self, titulo, artista, duracion, genero="Desconocido"):
        self.titulo = titulo      # Datos de la canción
        self.artista = artista    # Datos de la canción
        self.duracion = duracion  # Datos de la canción
        self.genero = genero      # Datos de la canción
        self.siguiente = None     # PUNTERO al siguiente nodo (característica de lista enlazada)
```
## 2. Clase Playlist (La lista enlazada)
```
python
class Playlist:
    def __init__(self, nombre):
        self.inicio = None    # Puntero al primer nodo
        self.actual = None    # Puntero al nodo actual (reproduciendo)
        self.tamaño = 0       # Contador de nodos
```
### Cómo funciona la lista enlazada:
```
text
[INICIO] → [Nodo 1] → [Nodo 2] → [Nodo 3] → ... → [Nodo N] → NULL
   ↑           ↑
(Playlist)   (Cada canción tiene .siguiente)
```
## Operaciones de Lista Enlazada Implementadas:
### 1. Inserción (Añadir al final)
```
python
def añadir_cancion(self, titulo, artista, duracion, genero):
    nueva_cancion = NodoCancion(titulo, artista, duracion, genero)  # Crear nuevo nodo
    
    if self.esta_vacia():
        self.inicio = nueva_cancion  # Primer nodo
    else:
        actual = self.inicio
        while actual.siguiente is not None:  # Recorrer hasta el último nodo
            actual = actual.siguiente
        actual.siguiente = nueva_cancion  # Enlazar nuevo nodo al final
```
### 2. Eliminación (Por posición)
```
python
def eliminar_posicion(self, posicion):
    if posicion == 1:  # Eliminar primer nodo
        eliminada = self.inicio
        self.inicio = self.inicio.siguiente  # Saltar al siguiente nodo
    else:  # Eliminar nodo intermedio
        anterior = self.inicio
        actual = self.inicio.siguiente
        while actual is not None:
            if contador == posicion:
                anterior.siguiente = actual.siguiente  # Saltar el nodo a eliminar
                break
```
### 3. Recorrido (Mostrar lista)
```
python
def obtener_lista(self):
    lista = []
    actual = self.inicio  #  Empezar desde el inicio
    while actual is not None:  #  Recorrer hasta NULL
        lista.append(actual.titulo)  # Acceder a datos del nodo
        actual = actual.siguiente  #  Moverse al siguiente nodo
    return lista
```
### 4. Navegación (Siguiente/Anterior)
```
python
def siguiente(self):
    if self.actual.siguiente is not None:
        self.actual = self.actual.siguiente  #  Avanzar al siguiente nodo
    else:
        self.actual = self.inicio  #  Volver al inicio (comportamiento circular)

def anterior(self):
    # Para retroceder en lista simple, debemos recorrer desde el inicio
    anterior = self.inicio
    while anterior.siguiente != self.actual:  # Buscar nodo anterior
        anterior = anterior.siguiente
    self.actual = anterior  # Establecer como actual
```
## Características de Lista Enlazada que se usan:
- Nodos con puntero siguiente

-  Inserción dinámica sin tamaño fijo

- Eliminación eficiente reorganizando punteros

- Recorrido secuencial desde el inicio

- Memoria dinámica (cada nodo se crea con new/malloc)

- No hay acceso aleatorio (solo secuencial)