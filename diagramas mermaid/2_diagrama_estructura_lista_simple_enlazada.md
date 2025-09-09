graph LR
    subgraph Playlist
        INICIO[inicio] --> N1[Nodo 1<br/>Bohemian Rhapsody]
        ACTUAL[actual] --> N3[Nodo 3<br/>Save Your Tears]
    end
    
    N1 -->|siguiente| N2[Nodo 2<br/>Blinding Lights]
    N2 -->|siguiente| N3
    N3 -->|siguiente| N4[Nodo 4<br/>Stairway to Heaven]
    N4 -->|siguiente| N5[Nodo 5<br/>Karma Police]
    N5 -->|siguiente| NULL[NULL]
    
    classDef current fill:#1DB954,color:white;
    class N3 current;