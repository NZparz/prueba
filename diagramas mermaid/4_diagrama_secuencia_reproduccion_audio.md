```mermaid
sequenceDiagram
    participant Usuario
    participant GUI
    participant Playlist
    participant PyGame

    Usuario->>GUI: Doble clic en canción
    GUI->>Playlist: establecer como actual
    Playlist->>Playlist: detener_audio()
    Playlist->>PyGame: music.stop()
    Playlist->>PyGame: music.load(archivo_mp3)
    Playlist->>PyGame: music.play()
    PyGame-->>Playlist: reproducción iniciada
    Playlist-->>GUI: confirmación reproducción
    GUI->>GUI: actualizar interfaz
    GUI-->>Usuario: mostrar canción actual```