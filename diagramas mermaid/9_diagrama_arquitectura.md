```mermaid
graph LR
    U[Usuario] --> GUI[Interfaz Gráfica]
    
    subgraph CapaPresentacion
        GUI --> Vistas[Vistas y Controles]
        Vistas --> Eventos[Manejo de Eventos]
    end
    
    subgraph CapaAplicacion
        Eventos --> Controlador[Controlador Principal]
        Controlador --> Servicios[Servicios de Audio]
        Controlador --> Ordenamiento[Servicios de Ordenamiento]
    end
    
    subgraph CapaDominio
        Servicios --> Playlist[Modelo Playlist]
        Ordenamiento --> Algoritmos[Algoritmos de Ordenamiento]
        Playlist --> Nodos[Modelo NodoCancion]
    end
    
    subgraph Infraestructura
        Servicios --> PyGame[Driver PyGame]
        Playlist --> Persistencia[Persistencia en Memoria]
        GUI --> Tkinter[Framework Tkinter]
    end
    
    PyGame --> S[System Sound]
    Tkinter --> OS[Sistema Operativo]```