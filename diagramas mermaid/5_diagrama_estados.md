```mermaid
stateDiagram-v2
    [*] --> Detenido

    state Detenido {
        [*] --> SinSeleccion
        SinSeleccion --> ConSeleccion : seleccionar canción
    }

    state Reproduciendo {
        [*] --> ReproduccionNormal
        ReproduccionNormal --> Pausado : pausar
        Pausado --> ReproduccionNormal : reanudar
        ReproduccionNormal --> [*] : fin canción
    }

    Detenido --> Reproduciendo : play/doble clic
    Reproduciendo --> Detenido : stop/cambiar canción
    
    state Finalizacion {
        [*] --> FinCancion
        FinCancion --> SiguienteCancion : auto-avance
        SiguienteCancion --> [*]
    }

    Reproduciendo --> Finalizacion : tiempo ≥ duración```