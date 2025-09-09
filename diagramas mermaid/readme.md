## 1. Diagrama de Clases del Sistema
Explicación: Muestra la estructura de clases principales. NodoCancion representa cada canción, Playlist gestiona la lista enlazada con operaciones CRUD y ordenamiento, y SpotifyStylePlayer maneja la interfaz gráfica. Las flechas muestran relaciones de composición y uso.

## 2. Diagrama de Estructura de Lista Simply Enlazada
Explicación: Ilustra cómo se conectan los nodos en memoria. Cada nodo apunta al siguiente, con punteros inicio y actual desde la playlist. El nodo actual se destaca visualmente mostrando la navegación en tiempo real.

## 3. Diagrama de Flujo del Algoritmo MergeSort
Explicación: Detalla el proceso "divide y vencerás" del MergeSort: dividir la lista recursivamente hasta tener nodos individuales, luego fusionarlos ordenadamente. Muestra la lógica de comparación y fusión que garantiza O(n log n).

## 4. Diagrama de Secuencia - Reproducción de Audio
Explicación: Secuencia temporal de acciones cuando el usuario reproduce una canción. Muestra la interacción entre componentes: GUI → Playlist → PyGame, con flujo de confirmaciones y actualizaciones de estado.

## 5. Diagrama de Estados del Reproductor
Explicación: Modela los estados posibles (Detenido, Reproduciendo, Pausado) y las transiciones entre ellos. Incluye el estado de finalización automática que triggers el avance a la siguiente canción.

## 6. Diagrama de Componentes del Sistema
Explicación: Arquitectura en capas: Frontend (GUI), Backend (lógica de negocio) y Dependencias externas. Muestra cómo se relacionan los módulos y qué tecnologías utiliza cada parte.

## 7. Diagrama de Flujo - Añadir Canción
Explicación: Flujo completo de añadir nueva canción: desde el diálogo de usuario, validación de datos, creación del nodo, inserción en la lista y actualización de la interfaz. Incluye manejo de errores.

## 8. Diagrama de Flujo - Eliminar Canción
Explicación: Proceso de eliminación con todas las validaciones: verificar lista no vacía, confirmación del usuario, reorganización de punteros y manejo especial cuando se elimina la canción actual.

## 9. Diagrama de Arquitectura Completa
Explicación: Arquitectura hexagonal con 4 capas: Presentación (GUI), Aplicación (Controladores), Dominio (Modelos y Algoritmos) e Infraestructura (Drivers externos). Muestra separación de concerns.

## 10. Diagrama de Casos de Uso
Explicación: Todos los escenarios de uso del sistema desde perspectiva de usuario. Descompone cada caso de uso en pasos específicos y muestra cómo el ordenamiento MergeSort se integra en los flujos.

## 11. Diagrama de Persistencia en Memoria
Explicación: Cómo se almacenan los datos en runtime: estructura de nodos enlazados, metadatos de la playlist y composición de cada nodo. Muestra la naturaleza dinámica de la asignación de memoria.

## 12. Diagrama de Ciclo de Vida del Reproductor
Explicación: Timeline completo de la aplicación desde inicio hasta terminación. Incluye fases de inicialización, operación normal, gestión de reproducción y shutdown ordenado.