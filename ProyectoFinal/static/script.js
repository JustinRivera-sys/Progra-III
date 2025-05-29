
// Collapsibles
document.querySelectorAll('.collapsible').forEach(btn=>{
  btn.addEventListener('click',function(){
    this.classList.toggle('active');
    const c=this.nextElementSibling;
    c.style.maxHeight = c.style.maxHeight ? null : c.scrollHeight+'px';
  });
});

// Leaflet setup
const map = L.map('map').setView([15.5,-90.25],7);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19}).addTo(map);

let markers=[],routingControls=[],lastRecommendations=[],entitiesMap={};

function clearMap(){
  markers.forEach(m=>map.removeLayer(m));
  routingControls.forEach(rc=>map.removeControl(rc));
  markers=[];routingControls=[];
}


function showRecommendations(data) {
  clearMap();
  lastRecommendations = data;
  const cont = document.getElementById('recommendations');
  cont.innerHTML = '';

  if (!data.length) {
    cont.innerHTML = '<p>No se encontraron recomendaciones.</p>';
    return;
  }

  const originId = data[0].origin;
  const originEnt = entitiesMap[originId];

  const origM = L.marker([originEnt.latitude, originEnt.longitude])
    .addTo(map)
    .bindPopup('<b>Origen:</b> ' + originEnt.name)
    .openPopup(); // muestra el popup del origen de inmediato

  markers.push(origM);

  let lastPoint = L.latLng(originEnt.latitude, originEnt.longitude);
  let html = '<h2>Recomendaciones</h2>';

  data.forEach((rec, i) => {
    const ent = rec.entity;

    html += `
      <div class="recommendation-item">
        <h3>${ent.name}</h3>
        <p>
          <b>ID:</b> ${ent.identifier}<br>
          <b>Precio:</b> ${ent.price}<br>
          <b>Calif:</b> ${ent.average_rating.toFixed(2)}<br>
          <b>Estadía:</b> ${ent.estimated_stay || 0} h<br>
          <b>Dist:</b> ${rec.travel_distance.toFixed(1)} km<br>
          <b>Viaje:</b> ${Math.round(rec.travel_time * 60)} min
        </p>
      </div>`;

    const popupContent = `
      <div>
        <strong>(${ent.identifier}) ${ent.name}</strong><br>
        <b>Precio:</b> ${ent.price} <br>
        <b>Calificación:</b> ${ent.average_rating.toFixed(2)} <br>
        <b>Estadía:</b> ${ent.estimated_stay || 0} h
      </div>`;

    const marker = L.marker([ent.latitude, ent.longitude])
      .addTo(map)
      .bindPopup(popupContent);

    marker.on('click', function () {
      this.openPopup();
    });

    markers.push(marker);

    const dest = L.latLng(ent.latitude, ent.longitude);

    const rc = L.Routing.control({
      waypoints: [lastPoint, dest],
      routeWhileDragging: false,
      addWaypoints: false,
      draggableWaypoints: false,
      createMarker: () => null, // Evita que Leaflet Routing agregue sus propios marcadores
      lineOptions: { styles: [{ opacity: 0.7, weight: 5 }] },
      show: false
    }).addTo(map);

    routingControls.push(rc);
    lastPoint = dest;
  });

  cont.innerHTML = html;

  const group = L.featureGroup(markers);
  map.fitBounds(group.getBounds().pad(0.3));
}


// Nuevo buildGraphNetwork sin overlap
function buildGraphNetwork(data) {
  const ids = [data[0].origin].concat(data.map(r => r.entity.identifier));

  const nodes = ids.map(id => {
    const ent = entitiesMap[id];
    return {
      id,
      label: id === data[0].origin ? 'Origen\n' + ent.name : ent.name,
      shape: 'dot',
      size: 20,
      font: { size: 14, color: '#000' },
      color: id === data[0].origin ? '#ff6666' : '#97C2FC',
    };
  });

  const edges = [];
  for (let i = 0; i < ids.length; i++) {
    for (let j = i + 1; j < ids.length; j++) {
      const a = ids[i], b = ids[j];
      const p1 = L.latLng(entitiesMap[a].latitude, entitiesMap[a].longitude),
            p2 = L.latLng(entitiesMap[b].latitude, entitiesMap[b].longitude);
      const d = (p1.distanceTo(p2) / 1000).toFixed(1);
      edges.push({
        from: a,
        to: b,
        label: `${d} km`,
        font: { size: 12, align: 'top' },
        smooth: { type: 'dynamic' }
      });
    }
  }

  const dataVis = {
    nodes: new vis.DataSet(nodes),
    edges: new vis.DataSet(edges)
  };

  const container = document.getElementById('network');
  new vis.Network(container, dataVis, {
    layout: {
      improvedLayout: true
    },
    physics: {
      enabled: true,
      solver: 'forceAtlas2Based',
      forceAtlas2Based: {
        gravitationalConstant: -50,
        centralGravity: 0.01,
        springLength: 120,
        springConstant: 0.08,
        avoidOverlap: 1
      },
      stabilization: {
        iterations: 200
      }
    },
    interaction: {
      hover: true
    }
  });
}

function buildAdjacencyMatrix(data) {
  const ids = [data[0].origin].concat(data.map(r => r.entity.identifier));
  const n = ids.length;
  const headers = ids.map(id => entitiesMap[id].name);
  const matrix = Array.from({ length: n }, () => Array(n).fill(0));

  for (let i = 0; i < n; i++) {
    for (let j = 0; j < n; j++) {
      if (i !== j) {
        const a = entitiesMap[ids[i]];
        const b = entitiesMap[ids[j]];
        const d = (L.latLng(a.latitude, a.longitude).distanceTo(
                     L.latLng(b.latitude, b.longitude)) / 1000).toFixed(1);
        matrix[i][j] = d;
      }
    }
  }

  buildAdjacencyTable(headers, matrix);
}


function buildAdjacencyTable(headers, matrix) {
  const container = document.getElementById('adjacency-matrix');
  container.innerHTML = ''; // Limpia contenido previo

  const table = document.createElement('table');
  table.classList.add('adj-matrix');

  // Encabezado
  const thead = document.createElement('thead');
  const headRow = document.createElement('tr');
  headRow.appendChild(document.createElement('th')); // Celda vacía inicial
  headers.forEach(h => {
    const th = document.createElement('th');
    th.textContent = h;
    headRow.appendChild(th);
  });
  thead.appendChild(headRow);
  table.appendChild(thead);

  // Cuerpo
  const tbody = document.createElement('tbody');
  matrix.forEach((row, i) => {
    const tr = document.createElement('tr');
    const label = document.createElement('th');
    label.textContent = headers[i];
    tr.appendChild(label);
    row.forEach(val => {
      const td = document.createElement('td');
      td.textContent = val;
      tr.appendChild(td);
    });
    tbody.appendChild(tr);
  });

  table.appendChild(tbody);
  container.appendChild(table);
}



document.getElementById('show-graph-btn').addEventListener('click',()=>{
  const nc=document.getElementById('network-container');
  nc.style.maxHeight=nc.style.maxHeight?null:nc.scrollHeight+'px';
  if(lastRecommendations.length) buildGraphNetwork(lastRecommendations);
});


document.getElementById('show-matrix-btn').addEventListener('click', () => {
  const mc = document.getElementById('matrix-container');
  mc.style.maxHeight = mc.style.maxHeight ? null : mc.scrollHeight + 'px';
  if (lastRecommendations.length) {
    buildAdjacencyMatrix(lastRecommendations);
  }
});


async function loadDataTable(){
  const res=await fetch('/get_entities'), js=await res.json();
  entitiesMap=Object.fromEntries(js.entities.map(e=>[e.identifier,e]));
  const tb=document.getElementById('data-table-body');
  tb.innerHTML='';
  js.entities.sort((a,b)=>+a.identifier-+b.identifier).forEach(e=>{
    const tr=document.createElement('tr');
    tr.innerHTML=`
      <td>${e.identifier}</td><td>${e.name}</td><td>${e.entity_type}</td>
      <td>${e.latitude}</td><td>${e.longitude}</td>
      <td>${e.price}</td><td>${e.average_rating.toFixed(2)}</td>
      <td>${e.estimated_stay||'N/A'}</td>`;
    tb.appendChild(tr);
  });
}

document.getElementById('upload-places').onsubmit=async e=>{
  e.preventDefault();
  const f=document.getElementById('file-places');
  if(!f.files.length) return alert('Seleccione CSV');
  const fd=new FormData(); fd.append('file',f.files[0]);
  const r=await fetch('/upload_entities',{method:'POST',body:fd});
  alert(await r.text()); if(r.ok) await loadDataTable();
};
document.getElementById('upload-ratings').onsubmit=async e=>{
  e.preventDefault();
  const f=document.getElementById('file-ratings');
  if(!f.files.length) return alert('Seleccione CSV');
  const fd=new FormData(); fd.append('file',f.files[0]);
  const r=await fetch('/upload_ratings',{method:'POST',body:fd});
  alert((await r.json()).message); await loadDataTable();
};
document.getElementById('recommend-form').onsubmit=async e=>{
  e.preventDefault();
  const origin=document.getElementById('origin').value.trim(),
        budget=parseFloat(document.getElementById('budget').value);
  if(!origin||isNaN(budget)||budget<=0) return alert('Datos inválidos');
  const r=await fetch('/recommend',{
    method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({origin,budget})
  });
  const js=await r.json();
  if(js.error) return alert(js.error);
  if(js.recommendations.length) js.recommendations[0].origin=origin;
  showRecommendations(js.recommendations);
};
document.getElementById('manual-form').onsubmit=async e=>{
  e.preventDefault();
  const data={}; new FormData(e.target).forEach((v,k)=>data[k]=v);
  const r=await fetch('/add_manual',{method:'POST',
    headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
  alert(await r.text()); if(r.ok){e.target.reset();await loadDataTable();}
};
document.getElementById('show-data-btn').addEventListener('click',loadDataTable);


document.getElementById('export-pdf-btn').addEventListener('click', async () => {
  const { jsPDF } = window.jspdf;
  const doc = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' });

  // Captura del contenedor de recomendaciones
  const recommendations = document.getElementById('recommendations');
  const canvas = await html2canvas(recommendations, { scale: 2 });
  const imgData = canvas.toDataURL('image/png');
  const imgProps = doc.getImageProperties(imgData);
  const pdfWidth = 190; // A4 ancho - márgenes
  const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;

  doc.addImage(imgData, 'PNG', 10, 10, pdfWidth, pdfHeight);

  // Captura del contenedor de la matriz
  const matrix = document.getElementById('matrix-container');
  if (matrix && matrix.scrollHeight > 0) {
    const canvasMatrix = await html2canvas(matrix, { scale: 2 });
    const matrixImgData = canvasMatrix.toDataURL('image/png');
    doc.addPage();
    doc.addImage(matrixImgData, 'PNG', 10, 10, pdfWidth, (canvasMatrix.height * pdfWidth) / canvasMatrix.width);
  }

  // Captura del grafo de vis.js
  const network = document.getElementById('network-container');
  if (network && network.scrollHeight > 0) {
    const canvasGraph = await html2canvas(network, { scale: 2 });
    const graphImgData = canvasGraph.toDataURL('image/png');
    doc.addPage();
    doc.addImage(graphImgData, 'PNG', 10, 10, pdfWidth, (canvasGraph.height * pdfWidth) / canvasGraph.width);
  }

  doc.save('reporte_recomendaciones.pdf');
});

const marker = L.marker([lat, lng]).addTo(map).bindPopup('Texto del popup');

marker.on('popupopen', () => {
  const popupContent = document.querySelector('.leaflet-popup-content');
  if (popupContent) {
    popupContent.style.backgroundColor = 'yellow';
  }
});


