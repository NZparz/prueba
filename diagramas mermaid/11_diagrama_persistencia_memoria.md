```mermaid
graph LR
    APP[Aplicación] --> PL[Playlist]
    PL --> N1[Nodo 1]
    PL --> N2[Nodo 2]
    PL --> N3[Nodo 3]
    
    N1 -->|siguiente| N2
    N2 -->|siguiente| N3
    N3 -->|siguiente| NULL[NULL]
    
    subgraph Metadatos
        PL --> MD1[nombre: String]
        PL --> MD2[tamaño: int]
        PL --> MD3[actual: Nodo]
        PL --> MD4[reproduciendo: bool]
    end
    
    subgraph DatosCancion
        N1 --> DC1[titulo: String]
        N1 --> DC2[artista: String]
        N1 --> DC3[duración: int]
        N1 --> DC4[archivo: String]
        N1 --> DC5[siguiente: Nodo]
    end```