```mermaid
flowchart TD
    A[Usuario: Click Eliminar] --> B{¿Lista vacía?}
    B -->|Sí| C[Mostrar error]
    B -->|No| D{¿Hay selección?}
    D -->|No| E[Mostrar error]
    D -->|Sí| F[Confirmar eliminación]
    
    F -->|Cancelar| G[Fin]
    F -->|Aceptar| H[Obtener posición]
    H --> I{¿Primer nodo?}
    I -->|Sí| J[Eliminar primer nodo]
    I -->|No| K[Buscar nodo anterior]
    K --> L[Reorganizar punteros]
    
    J --> M[Decrementar tamaño]
    L --> M
    
    M --> N{¿Era nodo actual?}
    N -->|Sí| O[Reestablecer nodo actual]
    N -->|No| P[Actualizar lista]
    
    O --> P
    P --> Q[Mostrar confirmación]
    Q --> R[Fin]
    
    C --> R
    E --> R```