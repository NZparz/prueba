```mermaid
graph TB
    subgraph Frontend[Interfaz Gráfica]
        GUI[SpotifyStylePlayer]
        STYLES[Estilos y Temas]
        CONTROLS[Controles de UI]
    end

    subgraph Backend[Lógica de Negocio]
        PL[Playlist Management]
        LL[Lista Simply Enlazada]
        MS[MergeSort Algorithm]
        AM[Audio Manager]
    end

    subgraph External[Dependencias Externas]
        PYGame[PyGame Mixer]
        TK[Tkinter]
        OS[Sistema Archivos]
    end

    GUI --> PL
    GUI --> STYLES
    GUI --> CONTROLS
    
    PL --> LL
    PL --> MS
    PL --> AM
    
    AM --> PYGame
    GUI --> TK
    PL --> OS

    classDef front fill:#3498db,color:white;
    classDef back fill:#2ecc71,color:white;
    classDef ext fill:#e74c3c,color:white;
    
    class GUI,STYLES,CONTROLS front;
    class PL,LL,MS,AM back;
    class PYGame,TK,OS ext;```