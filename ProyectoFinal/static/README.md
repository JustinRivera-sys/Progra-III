Este script permite cargar datos desde archivos CSV, generar recomendaciones personalizadas en un mapa con Leaflet, construir grafos con `vis.js`, crear matrices de adyacencia y exportar los resultados en un PDF.

---

## 📁 Funcionalidades

### 1. Interfaz Interactiva

- Desplegables (`.collapsible`) para expandir secciones dinámicamente.
- Interacción con el DOM para manejar formularios y botones.

```js
document.querySelectorAll('.collapsible').forEach(btn => {
  btn.addEventListener('click', function () {
    this.classList.toggle('active');
    const c = this.nextElementSibling;
    c.style.maxHeight = c.style.maxHeight ? null : c.scrollHeight + 'px';
  });
});
```

---

### 🗺️ Mapa con Leaflet
Inicializa el mapa centrado en Guatemala:

```js
const map = L.map('map').setView([15.5, -90.25], 7);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19 }).addTo(map);
```

---

### Limpiar el Mapa

```js
function clearMap() {
  markers.forEach(m => map.removeLayer(m));
  routingControls.forEach(rc => map.removeControl(rc));
  markers = [];
  routingControls = [];
}
```

---

### 💡 Mostrar Recomendaciones
Muestra entidades recomendadas en el mapa y genera una lista detallada.

```js
function showRecommendations(data) {
  // Lógica para mostrar marcadores, rutas y panel HTML
}
```

---

### 🌐 Visualización de Grafos

Utiliza `vis.js` para construir un grafo entre los puntos de recomendación:

```js
function buildGraphNetwork(data) {
  // Crea nodos y aristas con distancias geográficas
}

```
- Parámetros del grafo:
  - Algoritmo: forceAtlas2Based
  - Evita solapamiento automático
  - Muestra etiquetas con distancias en km

---

### 🧮 Matriz de Adyacencia
Genera una tabla de distancias entre todas las entidades mostradas:
```js
function buildAdjacencyMatrix(data) {
  // Crea matriz a partir de coordenadas geográficas
}
```
Representación HTML generada dinámicamente con etiquetas y datos.

---

### 📤 Carga de Archivos CSV
Carga entidades y calificaciones mediante formularios:
```js
document.getElementById('upload-places').onsubmit = async e => { ... };
document.getElementById('upload-ratings').onsubmit = async e => { ... };
```
Utiliza `fetch` con `FormData` para enviar los archivos al backend.

---

### 🧾 Recomendaciones Personalizadas
Envía datos del formulario y recibe sugerencias del servidor:
```js
document.getElementById('recommend-form').onsubmit = async e => { ... };
```
Recibe una lista con distancias, precios, ratings, y muestra resultados.

---

### 🧑‍💻 Ingreso Manual
Permite agregar manualmente una entidad desde el formulario:
```js
document.getElementById('manual-form').onsubmit = async e => { ... };
```
Los datos se envían en formato JSON.

---

### 📊 Exportación a PDF
Captura las secciones visibles (recomendaciones, matriz, grafo) y las exporta a un archivo PDF:
```js
document.getElementById('export-pdf-btn').addEventListener('click', async () => {
  // Usa jsPDF + html2canvas para generar el PDF
});
```
- Incluye:
  - Contenedor de recomendaciones
  - Matriz de adyacencia
  - Grafo visual

---

### 📌 Ejemplo de Marcador Personalizado
```js
const marker = L.marker([lat, lng]).addTo(map).bindPopup('Texto del popup');
marker.on('popupopen', () => {
  const popupContent = document.querySelector('.leaflet-popup-content');
  if (popupContent) {
    popupContent.style.backgroundColor = 'yellow';
  }
});
```
