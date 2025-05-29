Este archivo HTML representa la interfaz principal del "Sistema de Recomendación Turística".
A continuación se explican las secciones clave del documento:

1. CABECERA DEL DOCUMENTO (HEAD)
   - Se define el título de la página y se incluyen las siguientes bibliotecas externas:
     - Leaflet y Leaflet Routing Machine: para mostrar mapas y rutas.
     - jsPDF y html2canvas: para exportar contenido como PDF.
     - vis-network: para mostrar grafos de relaciones entre lugares.
     - Bootstrap 5 y Font Awesome: para diseño moderno y uso de íconos.
     - Un archivo CSS personalizado desde la carpeta static.

2. INTERFAZ PRINCIPAL (BODY)
   - Encabezado con el título del sistema.
   - Dos formularios para cargar archivos CSV:
     - CSV de lugares turísticos.
     - CSV opcional de calificaciones.

3. FORMULARIO DE RECOMENDACIONES
   - Permite ingresar:
     - El ID de lugar de origen.
     - Un presupuesto diario.
   - Al enviar, se generan recomendaciones basadas en esos parámetros.

4. FORMULARIO PARA AGREGAR LUGARES MANUALMENTE
   - Opción para ingresar manualmente los datos de un lugar:
     - ID, nombre, tipo, coordenadas, precio, calificación y duración de estadía.

5. SECCIÓN DE RESULTADOS Y VISUALIZACIÓN
   - `#recommendations`: espacio donde se mostrarán los lugares recomendados.
   - `#map`: contenedor para visualizar los puntos y rutas en el mapa interactivo.
   - `#graph-section`: permite mostrar:
     - El grafo ponderado con vis-network.
     - La matriz de adyacencia.

6. BOTONES DE EXPORTACIÓN
   - Exportar la vista como PDF.
   - Descargar el Árbol B como imagen PNG.

7. TABLA DE DATOS
   - Permite visualizar los datos cargados o ingresados manualmente en una tabla.

8. SCRIPTS FINALES
   - Se enlaza un archivo `script.js` personalizado desde la carpeta static para manejar la lógica de interacción.

Este documento HTML forma parte de una aplicación Flask más amplia, donde las rutas de archivos CSS y JS están gestionadas dinámicamente por `url_for`.
