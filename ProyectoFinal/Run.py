import csv, io, math
from flask import Flask, render_template_string, request, jsonify, render_template, send_file 
from geopy.distance import geodesic 
from btree_visualizer import visualize_btree


app = Flask(__name__)
app.secret_key = 'clave-secreta'

# ---------- Árbol B ----------
class BTreeNode:
    def __init__(self, t, leaf=False):
        self.t = t
        self.leaf = leaf
        self.keys = [None] * (2*t - 1)
        self.values = [None] * (2*t - 1)
        self.children = [None] * (2*t)
        self.n = 0

class BTree:
    def __init__(self, t=3):
        self.root = BTreeNode(t, leaf=True)
        self.t = t

    def search(self, k, x=None):
        if x is None: x = self.root
        i = 0
        while i < x.n and k > x.keys[i]:
            i += 1
        if i < x.n and k == x.keys[i]:
            return x.values[i]
        elif x.leaf:
            return None
        else:
            return self.search(k, x.children[i])

    def insert(self, k, v):
        r = self.root
        if r.n == 2*self.t - 1:
            s = BTreeNode(self.t)
            s.leaf = False
            s.children[0] = r
            self.root = s
            self.split_child(s, 0)
            self._insert_nonfull(s, k, v)
        else:
            self._insert_nonfull(r, k, v)

    def _insert_nonfull(self, x, k, v):
        i = x.n - 1
        if x.leaf:
            while i >= 0 and k < x.keys[i]:
                x.keys[i+1] = x.keys[i]
                x.values[i+1] = x.values[i]
                i -= 1
            x.keys[i+1] = k
            x.values[i+1] = v
            x.n += 1
        else:
            while i >= 0 and k < x.keys[i]:
                i -= 1
            i += 1
            if x.children[i].n == 2*self.t - 1:
                self.split_child(x, i)
                if k > x.keys[i]:
                    i += 1
            self._insert_nonfull(x.children[i], k, v)

    def split_child(self, x, i):
        t = self.t
        y = x.children[i]
        z = BTreeNode(t, leaf=y.leaf)
        z.n = t-1
        for j in range(t-1):
            z.keys[j] = y.keys[j+t]
            z.values[j] = y.values[j+t]
        if not y.leaf:
            for j in range(t):
                z.children[j] = y.children[j+t]
        y.n = t-1
        for j in range(x.n, i, -1):
            x.children[j+1] = x.children[j]
        x.children[i+1] = z
        for j in range(x.n-1, i-1, -1):
            x.keys[j+1] = x.keys[j]
            x.values[j+1] = x.values[j]
        x.keys[i] = y.keys[t-1]
        x.values[i] = y.values[t-1]
        x.n += 1

    def traverse(self, x=None, arr=None):
        if arr is None: arr = []
        if x is None: x = self.root
        i = 0
        while i < x.n:
            if not x.leaf:
                self.traverse(x.children[i], arr)
            arr.append(x.values[i])
            i += 1
        if not x.leaf:
            self.traverse(x.children[i], arr)
        return arr

# ---------- Entidades ----------
class Entity:
    def __init__(self, identifier, name, entity_type, lat, lon, price, avg_rating):
        self.identifier = identifier
        self.name = name
        self.entity_type = entity_type
        self.latitude = lat
        self.longitude = lon
        self.price = price
        self.average_rating = avg_rating
        # si avg_rating>0, se considera como rating inicial
        self.user_ratings = [avg_rating] if avg_rating > 0 else []

    def add_rating(self, r):
        self.user_ratings.append(r)
        self.average_rating = sum(self.user_ratings) / len(self.user_ratings)

class TouristSpot(Entity):
    def __init__(self, identifier, name, lat, lon, price, avg_rating, est_stay):
        super().__init__(identifier, name, 'Turístico', lat, lon, price, avg_rating)
        self.estimated_stay = est_stay

class Hotel(Entity):
    def __init__(self, identifier, name, lat, lon, price, avg_rating):
        super().__init__(identifier, name, 'Hospedaje', lat, lon, price, avg_rating)

# ---------- Grafo y recomendación ----------
class WeightedGraph:
    def __init__(self):
        self.adj = {}

    def add_vertex(self, v):
        if v not in self.adj:
            self.adj[v] = {}

    def add_edge(self, u, v, w):
        self.adj.setdefault(u,{})[v] = w
        self.adj.setdefault(v,{})[u] = w

    def dijkstra(self, start):
        unvis = {v: math.inf for v in self.adj}
        unvis[start] = 0
        vis = {}
        while unvis:
            u = min(unvis, key=unvis.get)
            d = unvis[u]
            if d == math.inf: break
            for nbr, w in self.adj[u].items():
                if nbr not in vis:
                    nd = d + w
                    if nd < unvis.get(nbr, math.inf):
                        unvis[nbr] = nd
            vis[u] = d
            unvis.pop(u)
        return vis

entities_tree = BTree()
entities_map = {}
entities_ordered = []
graph = WeightedGraph()

def parse_float(v, d=0.0):
    try: return float(v)
    except: return d

def build_graph():
    global graph
    graph = WeightedGraph()
    for e in entities_ordered:
        graph.add_vertex(e.identifier)
    n = len(entities_ordered)
    for i in range(n):
        for j in range(i+1, n):
            e1 = entities_ordered[i]
            e2 = entities_ordered[j]
            dist = geodesic((e1.latitude,e1.longitude),(e2.latitude,e2.longitude)).km
            graph.add_edge(e1.identifier, e2.identifier, dist)

def score_place(entity, budget, time_left, travel_time):
    if entity.price > budget:
        return -1
    total_time = (entity.estimated_stay if entity.entity_type=='Turístico' else 0) + travel_time
    if total_time > time_left:
        return -1
    return entity.average_rating*2 - entity.price/10 - total_time*0.5

def recommend_route(origin_id, budget, max_hours=8):
    if origin_id not in entities_map:
        return []
    visits = []
    budget_left = budget
    time_left = max_hours
    current = origin_id
    visited = set()
    for _ in range(5):
        dists = graph.dijkstra(current)
        cands = []
        for eid, dist in dists.items():
            if eid == current or eid in visited:
                continue
            ent = entities_map[eid]
            if ent.entity_type != 'Turístico':
                continue
            travel_time = dist / 30
            sc = score_place(ent, budget_left, time_left, travel_time)
            if sc > 0:
                cands.append((sc, ent, travel_time, dist))
        if not cands:
            break
        cands.sort(key=lambda x: x[0], reverse=True)
        _, ent, trav, dist = cands[0]
        visits.append({'entity': ent, 'travel_time': trav, 'travel_distance': dist})
        budget_left -= ent.price
        time_left -= ent.estimated_stay + trav
        current = ent.identifier
        visited.add(ent.identifier)
    return visits


@app.route('/')
def index():
    return render_template('index.html')

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

@app.route('/upload_ratings', methods=['POST'])
def upload_ratings():
    file = request.files.get('file')
    if not file:
        return jsonify(message="No se encontró el archivo"), 400
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

@app.route('/download_btree')
def download_btree():
    dot = visualize_btree(entities_tree)
    output_path = "/tmp/btree_graph"
    dot.render(output_path, cleanup=True)
    return send_file(output_path + '.png', as_attachment=True, download_name='arbol_b.png')



if __name__ == '__main__':
    app.run(debug=True)