```mermaid
flowchart TD
    U[Usuario] --> UC1[Reproducir canción]
    U --> UC2[Pausar/Reanudar]
    U --> UC3[Siguiente/Anterior]
    U --> UC4[Añadir canción]
    U --> UC5[Eliminar canción]
    U --> UC6[Ordenar playlist]
    U --> UC7[Ajustar volumen]
    
    UC1 --> MS1[Seleccionar canción]
    UC1 --> MS2[Cargar audio]
    UC1 --> MS3[Reproducir]
    
    UC4 --> MS4[Validar datos]
    UC4 --> MS5[Crear nodo]
    UC4 --> MS6[Enlazar nodo]
    
    UC6 --> MS7[Ejecutar MergeSort]
    UC6 --> MS8[Reorganizar lista]
    UC6 --> MS9[Actualizar vista]
    
    subgraph MergeSortProcess
        MS7 --> DIV[Dividir lista]
        DIV --> ORD[Ordenar recursivamente]
        ORD --> FUS[Fusionar mitades]
        FUS --> ORD
    end```