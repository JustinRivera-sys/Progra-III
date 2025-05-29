
# 🌐 Proyecto Final: Sistema de Recomendación Turística
## 👥 Integrantes 
- **Justin Daniel Rivera López**   – 9490-23-10643  – 100%  
- **Marco Tulio Pineda Recinos**   – 9490-23-2906   – 100%  
- **Brayan Kenet Rivera Quinilla** – 9490-23-2835   – 100%
---
## 🎯 Objetivo del Proyecto

Desarrollar una aplicación que permita a los usuarios obtener **recomendaciones de rutas turísticas** desde un punto de origen, considerando:

- Tiempo disponible  
- Distancia entre sitios  
- Calificaciones de los lugares  
- Presupuesto diario  

El sistema permitirá:

- La **carga masiva** de lugares turísticos y hospedajes  
- La **recomendación optimizada** de sitios a visitar cada día

---

> [!WARNING]  
> Solo se debe ejecutar el archivo:  
> `Run.py`


> [!IMPORTANT]  
> Antes de ejecutar por primera vez, abrir una terminal y correr:
> ```bash
> pip install Flask
> pip install geopy
> pip install btree-visualizer
> ```

> [!NOTE]  
> - `Flask`: permite mostrar la página HTML, recibir datos y enviar archivos para descargar  
> - `geopy`: calcula distancias entre coordenadas geográficas  
> - `btree-visualizer`: permite visualizar el Árbol B generado  

---

## ⚙️ Funcionalidades principales

### 1. `/upload_entities`
Carga entidades turísticas desde un archivo `.csv`.  
El archivo debe contener:
- Identificador
- Nombre
- Tipo (Hotel o Turístico)
- Latitud y Longitud
- Precio
- Calificación promedio
- Tiempo estimado de estadía

```Python
@app.route('/upload_entities', methods=['POST'])
def upload_entities():
    global entities_map, entities_ordered, entities_tree
    file = request.files.get('file')
    if not file:
        return "Archivo no encontrado", 400
    entities_tree = BTree()
    entities_map = {}
    entities_ordered = []
    stream = io.StringIO(file.stream.read().decode('ISO-8859-1'), newline=None)
    reader = csv.DictReader(stream)
    count = 0
    for row in reader:
        try:
            id_, name = row['Identificador'].strip(), row['Nombre'].strip()
            tipo = row['Tipo'].strip().lower()
            lat = parse_float(row.get('Latitud',0))
            lon = parse_float(row.get('Longitud',0))
            price = parse_float(row.get('Precio',0))
            avg = parse_float(row.get('Calificacion promedio',0))
            if 'hospedaje' in tipo or tipo=='hotel':
                ent = Hotel(id_, name, lat, lon, price, avg)
            else:
                est = parse_float(row.get('Tiempo estimado de estadia',0))
                ent = TouristSpot(id_, name, lat, lon, price, avg, est)
            entities_tree.insert(id_, ent)
            entities_map[id_] = ent
            entities_ordered.append(ent)
            count += 1
        except:
            continue
    entities_ordered.sort(key=lambda x:int(x.identifier))
    build_graph()
    return f"Cargados {count} lugares correctamente."
```

---

### 2. `/upload_ratings`
Carga calificaciones de los usuarios por entidad.  
Recalcula el promedio por entidad y actualiza el Árbol B.

```Python
@app.route('/upload_ratings', methods=['POST'])
def upload_ratings():
    file = request.files.get('file')
    if not file:
        return jsonify(message="No se encontró el archivo"), 400

    # Leer todo el contenido con cualquiera de las codificaciones comunes
    data = file.read()
    s = None
    for enc in ('utf-8', 'latin-1', 'ISO-8859-1'):
        try:
            s = data.decode(enc)
            break
        except:
            continue
    if s is None:
        return jsonify(message="Error de codificación"), 400

    # Agrupar calificaciones por entidad
    reader = csv.DictReader(io.StringIO(s))
    ratings_dict = {}
    total_rows = 0
    for row in reader:
        total_rows += 1
        id_ = row.get('Identificador de la entidad', '').strip()
        try:
            r = float(row.get('Calificación del usuario', ''))
        except:
            continue
        ratings_dict.setdefault(id_, []).append(r)

    # Aplicar reemplazo de calificaciones
    updated = 0
    skipped = 0
    for id_, ratings in ratings_dict.items():
        ent = entities_map.get(id_)
        if ent:
            ent.user_ratings = ratings[:]  # sobreescribe todas las anteriores
            ent.average_rating = sum(ratings) / len(ratings)
            updated += len(ratings)
        else:
            skipped += len(ratings)

    return jsonify(message=f"Calificaciones aplicadas: {updated}, Omitidas: {skipped}"), 200
```

---

### 3. `/recommend`
Calcula una ruta turística optimizada desde un punto de origen.  
Requiere:
- Identificador de origen
- Presupuesto diario

Devuelve hasta 5 recomendaciones según:
- Precio
- Calificación
- Distancia
- Tiempo estimado

```Python
@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    origin = data.get('origin')
    budget = data.get('budget')
    if origin not in entities_map:
        return {"error": "ID de origen no encontrado"}, 404
    recs = recommend_route(origin, budget)
    out = []
    for rec in recs:
        e = rec['entity']
        out.append({
            "entity": {
                "identifier": e.identifier,
                "name": e.name,
                "latitude": e.latitude,
                "longitude": e.longitude,
                "price": e.price,
                "average_rating": e.average_rating,
                "estimated_stay": getattr(e, "estimated_stay", None)
            },
            "travel_distance": rec['travel_distance'],
            "travel_time": rec['travel_time']
        })
    return {"recommendations": out}
```
---

### 4. `/add_manual`
Agrega una entidad manualmente (por JSON).  

```Python
@app.route('/add_manual', methods=['POST'])
def add_manual():
    data = request.json
    id_ = data['identifier']
    if id_ in entities_map:
        return "Error: ID ya existe", 400
    lat = parse_float(data.get('latitude', 0))
    lon = parse_float(data.get('longitude', 0))
    price = parse_float(data.get('price', 0))
    avg = parse_float(data.get('average_rating', 0))
    if data['entity_type'] == 'Turístico':
        est = parse_float(data.get('estimated_stay', 0))
        ent = TouristSpot(id_, data['name'], lat, lon, price, avg, est)
    else:
        ent = Hotel(id_, data['name'], lat, lon, price, avg)
    entities_tree.insert(id_, ent)
    entities_map[id_] = ent
    entities_ordered.append(ent)
    entities_ordered.sort(key=lambda x: int(x.identifier))
    build_graph()
    return "Lugar agregado exitosamente", 200
```

Ejemplo:
```json
{
  "Identificador": "191",
  "Nombre": "El Quetzal",
  "Tipo": "Turístico",
  "Latitud": 14.7667,
  "Longitud": -91.8167,
  "Precio": 100,
  "Calificaiones promedio": 4.7,
  "Tiempo estimado de estadia": 1.5
}
```

### 5. `/get_entities`
Devuelve un listado ordenado de todas las entidades cargadas.

```Python
@app.route('/get_entities', methods=['GET'])
def get_entities():
    serial = []
    for e in sorted(entities_ordered, key=lambda x: int(x.identifier)):
        serial.append({
            "identifier": e.identifier,
            "name": e.name,
            "entity_type": e.entity_type,
            "latitude": e.latitude,
            "longitude": e.longitude,
            "price": e.price,
            "average_rating": e.average_rating,
            "estimated_stay": getattr(e, "estimated_stay", None)
        })
    return jsonify(entities=serial)
```

---

### 6. `/download_btree`
Genera una imagen `.png` visual del Árbol B actual.
Disponible para descarga.
```Python
@app.route('/download_btree')
def download_btree():
    dot = visualize_btree(entities_tree)
    output_path = "/tmp/btree_graph"
    dot.render(output_path, cleanup=True)
    return send_file(output_path + '.png', as_attachment=True, download_name='arbol_b.png')
```

---

### 7. `btree_visualizer.py`
Genera la imagen de como esta construido el Arbol B

```Python
from graphviz import Digraph

def visualize_btree(btree):
    dot = Digraph(format='png')
    node_id = [0]

    def add_node(node):
        current_id = str(node_id[0])
        label_parts = []
        for i in range(node.n):
            label_parts.append(f"<f{i}> {node.keys[i]}")
        label = " | ".join(label_parts)
        dot.node(current_id, f'{{{label}}}', shape='record')
        node_id[0] += 1

        if not node.leaf:
            for i in range(node.n + 1):
                child = node.children[i]
                child_id = str(node_id[0])
                add_node(child)
                dot.edge(current_id + f":f{i}", child_id)

    add_node(btree.root)
    return dot
```

---

# Codigo en Ejecucion

> [!NOTE]  
> - Presionar `Ctrl` + `Click` en `http://127.0.0.1:5000`, para abrir una pestaña del navegador y ver el programa ya en ejecucion
> - Nos redirigira al navegador

![Image](https://github.com/user-attachments/assets/f3d30ce3-54ba-4cdc-8b3f-e18ecbaa97b3)

---

### Opciones que permite el progra
- Carga masiva de lugares
- Carga masiva de calificaiones
  - La `Carga masiva de calificaciones`, es opcional, si se agregar hace un promedio de los lugares que ya tienen calificaciones y les da otro valor
- Marcar un punto de origen con presupuesto diario, para ver las posibles recomendaciones
- Agregar un lugar manualmente
  - Tener en cuenta seguir con la numeracion que esta debajo en el boton: `Mostrar Datos`
- Mapa iteractivo que permite la visualizacion del punto de partida y los lugares recomendados
- #### BOTONES
  - `Mostrar Grafo ponderado`: da una visualizacion grafica de un `Grafo Ponderado`
  - `Mostrar Matriz de Adyacencia`: da una tabla que permite la visualizacion de como estaria relacionado los lugares
  - `Exporta como PDF`: crea un archivo pdf, guardando dentro los lugares recomendados, el grafo ponderado y la matriz de adyacencia
  - `Descargar Arbol B (PNG)`: crea un archivo pdf, donde se puede ver como esta almacenada la informacion de `carga masiva de lugares` y como se construye un `Arbol B` en memoria volatil
  - `Mostrar Datos`: nos permite ver todos los datos agregados gracias a `carga masiva de lugares` y `agregar manualmente` 
 
![Image](https://github.com/user-attachments/assets/a3151621-3a1a-43a3-a6bc-deb468cb27f6)
![Image](https://github.com/user-attachments/assets/be1a916f-6578-4823-96b0-513f526bf6e4)
![Image](https://github.com/user-attachments/assets/67f6f479-3a2b-440b-a6a9-9b9576d11714)

### Imagen de como esta armado el `Arbol B`
![Image](https://github.com/user-attachments/assets/94691018-0113-4c00-8528-604be73023a2)
