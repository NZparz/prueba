```mermaid
flowchart TD
    A[Usuario: Click Añadir] --> B[Mostrar diálogo]
    B --> C{Usuario completa datos}
    C -->|Cancelar| D[Cerrar diálogo]
    C -->|Aceptar| E[Validar datos]
    
    E --> F{¿Datos válidos?}
    F -->|No| G[Mostrar error]
    F -->|Sí| H[Crear nuevo NodoCancion]
    
    H --> I{¿Lista vacía?}
    I -->|Sí| J[Establecer como inicio y actual]
    I -->|No| K[Recorrer hasta último nodo]
    K --> L[Enlazar nuevo nodo]
    
    L --> M[Incrementar tamaño]
    M --> N[Actualizar Treeview]
    N --> O[Cerrar diálogo]
    O --> P[Mostrar mensaje éxito]
    
    G --> B
    D --> Q[Fin]
    P --> Q```