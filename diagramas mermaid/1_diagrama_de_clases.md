
```mermaid
classDiagram
    class NodoCancion {
        -String titulo
        -String artista
        -int duracion
        -String genero
        -String archivo_audio
        -NodoCancion siguiente
        +__init__(titulo, artista, duracion, genero, archivo_audio)
        +__str__() String
        +formatear_duracion() String
    }

    class Playlist {
        -String nombre
        -NodoCancion inicio
        -NodoCancion actual
        -int tamaño
        -bool reproduciendo
        -bool pausado
        +esta_vacia() bool
        +añadir_cancion(titulo, artista, duracion, genero, archivo_audio) NodoCancion
        +eliminar_posicion(posicion) NodoCancion
        +ordenar_por_titulo()
        +ordenar_por_artista()
        +ordenar_por_duracion()
        +_merge_sort(cabeza, criterio) NodoCancion
        +_dividir_lista(cabeza) NodoCancion
        +_fusionar(izquierda, derecha, criterio) NodoCancion
        +obtener_lista() List
        +siguiente() NodoCancion
        +anterior() NodoCancion
        +reproducir_audio() bool
        +pausar_audio()
        +reanudar_audio()
        +detener_audio()
    }

    class SpotifyStylePlayer {
        -Tk root
        -dict colors
        -Playlist playlist
        -ttk.Style style
        -ttk.Treeview tree
        -StringVar now_playing_text
        -Button play_btn
        -Button remove_btn
        -Scale volumen_scale
        +__init__(root)
        +setup_styles()
        +setup_ui()
        +cargar_canciones_ejemplo()
        +actualizar_lista()
        +actualizar_info_cancion(cancion)
        +toggle_play()
        +siguiente()
        +anterior()
        +ajustar_volumen(value)
        +ordenar_por_titulo()
        +ordenar_por_artista()
        +ordenar_por_duracion()
        +on_double_click(event)
        +reproducir_seleccionada()
        +añadir_cancion()
        +eliminar_cancion()
    }

    Playlist "1" *-- "*" NodoCancion : contiene
    SpotifyStylePlayer "1" *-- "1" Playlist : utiliza```