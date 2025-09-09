```mermaid
flowchart TD
    A[Inicio MergeSort] --> B{Lista vacía o<br/>un elemento?}
    B -->|Sí| C[Retornar lista]
    B -->|No| D[Dividir lista en dos mitades<br/>algoritmo tortuga y liebre]
    
    D --> E[Ordenar mitad izquierda<br/>MergeSort recursivo]
    D --> F[Ordenar mitad derecha<br/>MergeSort recursivo]
    
    E --> G[Fusionar mitades ordenadas]
    F --> G
    
    subgraph Fusion[Proceso de Fusión]
        G --> H[Comparar primeros elementos]
        H --> I{Elemento izquierdo ≤ derecho?}
        I -->|Sí| J[Añadir izquierdo<br/>avanzar izquierda]
        I -->|No| K[Añadir derecho<br/>avanzar derecha]
        J --> L{¿Quedan elementos?}
        K --> L
        L -->|Sí| H
        L -->|No| M[Añadir elementos restantes]
    end
    
    M --> N[Lista completamente ordenada]
    N --> O[Actualizar puntero inicio]

    O --> P[Fin MergeSort] ```
