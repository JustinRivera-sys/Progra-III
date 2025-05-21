
  // Navigation tab switching
  const navButtons = document.querySelectorAll('nav button');
  const sections = document.querySelectorAll('main section');
  navButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      navButtons.forEach(b => {
        b.classList.remove('active');
        b.setAttribute('aria-selected', 'false');
      });
      btn.classList.add('active');
      btn.setAttribute('aria-selected', 'true');

      const module = btn.getAttribute('data-module');
      sections.forEach(section => {
        if (section.id === module) {
          section.classList.add('active');
          section.setAttribute('aria-hidden', 'false');
        } else {
          section.classList.remove('active');
          section.setAttribute('aria-hidden', 'true');
        }
      });
    });
  });

  // Utils
  function parseNumbers(text) {
    // Accepts comma or space separated numbers, discard empty
    return text.split(/[\s,]+/)
      .map(e => parseFloat(e))
      .filter(n => !isNaN(n));
  }

  // Estadística Descriptiva
  function calcularDescriptiva() {
    const text = document.getElementById('datos-desc').value;
    const nums = parseNumbers(text);
    const resElem = document.getElementById('resultado-desc');

    if (nums.length === 0) {
      resElem.textContent = 'Por favor ingresa datos numéricos válidos.';
      return;
    }

    const n = nums.length;
    const sum = nums.reduce((a,b) => a+b, 0);
    const mean = sum / n;

    const sorted = [...nums].sort((a,b) => a-b);
    const median = (n % 2 === 1) ? sorted[(n-1)/2] : (sorted[n/2 -1] + sorted[n/2])/2;

    // Mode calculation: count frequencies
    const freqMap = {};
    nums.forEach(num => freqMap[num] = (freqMap[num] || 0) +1);
    let maxFreq = 0;
    Object.values(freqMap).forEach(f => { if (f > maxFreq) maxFreq = f });
    const modes = Object.keys(freqMap)
      .filter(k => freqMap[k] === maxFreq)
      .map(k => parseFloat(k));
    const mode = (maxFreq > 1) ? modes.join(', ') : 'No hay moda';

    const variance = nums.reduce((acc,x) => acc + (x - mean) ** 2, 0) / n;
    const stdDev = Math.sqrt(variance);

    resElem.textContent =
      `Cantidad de datos: ${n}
Media: ${mean.toFixed(4)}
Mediana: ${median.toFixed(4)}
Moda: ${mode}
Varianza: ${variance.toFixed(4)}
Desviación estándar: ${stdDev.toFixed(4)}`;
  }

  // Función factorial (para binomial)
  function factorial(x) {
    if (x === 0) return 1;
    let f = 1;
    for (let i = 1; i <= x; i++) f *= i;
    return f;
  }

  // Combinación n sobre k
  function combinacion(n,k) {
    if (k > n) return 0;
    return factorial(n) / (factorial(k) * factorial(n-k));
  }

  // Distribución Binomial
  function probBinomial(n, p, k) {
    const comb = combinacion(n, k);
    return comb * Math.pow(p, k) * Math.pow(1-p, n-k);
  }

  // Distribución Poisson
  function probPoisson(lambda, k) {
    return (Math.pow(lambda, k) * Math.exp(-lambda)) / factorial(k);
  }

  function mostrarCamposProb() {
    const dist = document.getElementById('tipo-distribucion').value;
    document.getElementById('binomial-campos').style.display = dist === 'binomial' ? '' : 'none';
    document.getElementById('poisson-campos').style.display = dist === 'poisson' ? '' : 'none';
    document.getElementById('resultado-prob').textContent = '';
  }

  function calcularProbabilidad() {
    const dist = document.getElementById('tipo-distribucion').value;
    const resElem = document.getElementById('resultado-prob');
    if(dist === 'binomial') {
      const n = parseInt(document.getElementById('n-bin').value, 10);
      const p = parseFloat(document.getElementById('p-bin').value);
      const k = parseInt(document.getElementById('k-bin').value, 10);

      if (isNaN(n) || n <=0 || p < 0 || p > 1 || isNaN(k) || k < 0 || k > n) {
        resElem.textContent = 'Por favor ingresa valores válidos para n, p y k.';
        return;
      }

      const prob = probBinomial(n, p, k);
      resElem.textContent = `P(X = ${k}) en Binomial(n=${n}, p=${p}) = ${prob.toFixed(6)}`;
    } else if (dist === 'poisson') {
      const lambda = parseFloat(document.getElementById('lambda-poisson').value);
      const k = parseInt(document.getElementById('k-poisson').value, 10);
      if(isNaN(lambda) || lambda < 0 || isNaN(k) || k < 0) {
        resElem.textContent = 'Por favor ingresa valores válidos para λ y k.';
        return;
      }
      const prob = probPoisson(lambda, k);
      resElem.textContent = `P(X = ${k}) en Poisson(λ=${lambda}) = ${prob.toFixed(6)}`;
    }
  }

  // Distribución Normal Z (Función de distribución acumulada aproximada)
  function normCdf(z) {
    // Abramowitz & Stegun approximation
    const t = 1 / (1 + 0.2316419 * Math.abs(z));
    const d = 0.3989423 * Math.exp(-z*z/2);
    let prob = d * t * (0.3193815 + t*(-0.3565638 + t*(1.781478 + t*(-1.821256 + t*1.330274))));
    if (z > 0) prob = 1 - prob;
    return prob;
  }

  // Función t inversa para alfa/2 usando aproximación para df>30
  // For simplicity, approximate with Z critical values for alpha
  function tCritical(alpha, df) {
    // For df > 30, t ~ z quantiles
    const zAlpha2 = inverseNormCDF(1 - alpha/2);
    return zAlpha2;
  }

  function inverseNormCDF(p) {
    // Beasley-Springer/Moro approximation for inverse normal CDF for p in (0,1)
    // Source simplified. This is sufficient for approximate critical values.
    if (p <= 0 || p >= 1) return NaN;
    const a = [2.50662823884, -18.61500062529, 41.39119773534, -25.44106049637];
    const b = [-8.47351093090, 23.08336743743, -21.06224101826, 3.13082909833];
    const c = [0.3374754822726147, 0.9761690190917186, 0.1607979714918209,
               0.0276438810333863, 0.0038405729373609, 0.0003951896511919,
               0.0000321767881768, 0.0000002888167364, 0.0000003960315187];
    let x = p - 0.5;
    if (Math.abs(x) < 0.42) {
      const r = x * x;
      const num = a[0] + a[1]*r + a[2]*r*r + a[3]*r*r*r;
      const denom = 1 + b[0]*r + b[1]*r*r + b[2]*r*r*r + b[3]*r*r*r*r;
      return x * num / denom;
    } else {
      let r = p;
      if (x > 0) r = 1 - p;
      r = Math.log(-Math.log(r));
      let val = c[0] + c[1]*r + c[2]*r*r + c[3]*r*r*r + c[4]*r*r*r*r + c[5]*r*r*r*r*r + c[6]*r*r*r*r*r*r + c[7]*r*r*r*r*r*r*r + c[8]*r*r*r*r*r*r*r*r;
      return (x < 0) ? -val : val;
    }
  }

  // Pruebas de Hipótesis
  function calcularPruebaHipotesis() {
    const resElem = document.getElementById('resultado-hipo');
    let xBar = parseFloat(document.getElementById('media-muestra').value);
    let mu0 = parseFloat(document.getElementById('media-poblacion').value);
    let sigma = parseFloat(document.getElementById('desv-estandar').value);
    let n = parseInt(document.getElementById('tamaño-muestra').value, 10);
    let alpha = parseFloat(document.getElementById('nivel-significancia').value);
    let tipo = document.getElementById('tipo-prueba').value;
    let cola = document.getElementById('cola-prueba').value;

    if ([xBar, mu0, sigma, n, alpha].some(v => isNaN(v) || v < 0)) {
      resElem.textContent = 'Por favor ingresa valores numéricos válidos y positivos.';
      return;
    }
    if (alpha <= 0 || alpha >= 1) {
      resElem.textContent = 'El nivel de significancia α debe estar entre 0 y 1.';
      return;
    }
    if (n < 1) {
      resElem.textContent = 'El tamaño de muestra debe ser al menos 1.';
      return;
    }

    const se = sigma / Math.sqrt(n);
    const z = (xBar - mu0) / se;

    let pValue = 0;
    if (cola === 'two') {
      pValue = 2 * (1 - normCdf(Math.abs(z)));
    } else if (cola === 'right') {
      pValue = 1 - normCdf(z);
    } else {
      pValue = normCdf(z);
    }

    // Decide rechazo o no
    let decision = '';
    if (pValue < alpha) {
      decision = 'Rechazamos la hipótesis nula.';
    } else {
      decision = 'No hay evidencia suficiente para rechazar la hipótesis nula.';
    }

    resElem.textContent = 
`Estadístico de prueba = ${z.toFixed(4)}
Valor p (p-value) = ${pValue.toFixed(4)}
Nivel de significancia α = ${alpha}
Decisión: ${decision}`;

  }

  // Intervalos de confianza
  function calcularIntervaloConfianza() {
    const resElem = document.getElementById('resultado-ic');
    let xBar = parseFloat(document.getElementById('media-ic').value);
    let s = parseFloat(document.getElementById('desv-ic').value);
    let n = parseInt(document.getElementById('n-ic').value, 10);
    let conf = parseFloat(document.getElementById('confianza-ic').value);
    let tipo = document.getElementById('tipo-ic').value;

    if ([xBar, s, n, conf].some(v => isNaN(v) || v < 0)) {
      resElem.textContent = 'Por favor ingresa valores numéricos válidos y positivos.';
      return;
    }
    if (conf <= 50 || conf >= 100) {
      resElem.textContent = 'El nivel de confianza debe estar entre 50% y 99.9%.';
      return;
    }
    if (n < 1) {
      resElem.textContent = 'El tamaño de muestra debe ser al menos 1.';
      return;
    }
    const alpha = 1 - conf / 100;

    // Z critical value approx
    const z = inverseNormCDF(1 - alpha / 2);

    if (tipo === 'z') {
      const se = s / Math.sqrt(n);
      const margen = z * se;
      const li = xBar - margen;
      const ls = xBar + margen;
      resElem.textContent = 
`Intervalo de confianza para la media (Z)
Nivel de confianza: ${conf}%
Intervalo: [${li.toFixed(4)}, ${ls.toFixed(4)}]`;
    } else if (tipo === 't') {
      // Approximate t critical as z for demo (could add full t dist later)
      const tcrit = tCritical(alpha, n -1);
      const se = s / Math.sqrt(n);
      const margen = tcrit * se;
      const li = xBar - margen;
      const ls = xBar + margen;
      resElem.textContent = 
`Intervalo de confianza para la media (T)
Nivel de confianza: ${conf}%
Aproximación con valor crítico: ${tcrit.toFixed(4)}
Intervalo: [${li.toFixed(4)}, ${ls.toFixed(4)}]`;
    } else if (tipo === 'p') {
      // Para proporciones, s is pHat, n sample size
      const pHat = s;
      const se = Math.sqrt(pHat * (1 - pHat) / n);
      const margen = z * se;
      const li = pHat - margen;
      const ls = pHat + margen;
      resElem.textContent = 
`Intervalo de confianza para proporción
Nivel de confianza: ${conf}%
Intervalo: [${li.toFixed(4)}, ${ls.toFixed(4)}]`;
    } else {
      resElem.textContent = 'Tipo de intervalo inválido.';
    }
  }

  // Regresión Lineal Simple
  function calcularRegresion() {
    const resElem = document.getElementById('resultado-reg');
    const xs = parseNumbers(document.getElementById('datos-x').value);
    const ys = parseNumbers(document.getElementById('datos-y').value);

    if (xs.length === 0 || ys.length === 0) {
      resElem.textContent = 'Por favor ingresa datos válidos para X e Y.';
      return;
    }
    if (xs.length !== ys.length) {
      resElem.textContent = 'Las series de datos X e Y deben tener la misma cantidad de elementos.';
      return;
    }
    const n = xs.length;
    const meanX = xs.reduce((a,b) => a+b, 0)/n;
    const meanY = ys.reduce((a,b) => a+b, 0)/n;

    let num = 0;
    let den = 0;
    let sst = 0;
    let ssr = 0;

    for (let i=0; i<n; i++) {
      num += (xs[i]-meanX)*(ys[i]-meanY);
      den += (xs[i]-meanX)**2;
    }

    if (den === 0) {
      resElem.textContent = 'No se puede calcular la regresión con la varianza de X igual a cero.';
      return;
    }

    const b1 = num/den;
    const b0 = meanY - b1*meanX;

    // Calcular R^2
    for (let i=0; i<n; i++) {
      const fit = b0 + b1*xs[i];
      ssr += (fit - meanY)**2;
      sst += (ys[i] - meanY)**2;
    }
    const r2 = sst > 0 ? ssr / sst : 1;

    resElem.textContent =
`Ecuación: ŷ = ${b0.toFixed(4)} + ${b1.toFixed(4)}x
Coeficiente de determinación R²: ${r2.toFixed(4)}`;
  }

let a = 0;
let b = 0;
let chartCuadrados;

function calcularCuadradosMinimos() {
  const xInput = document.getElementById('datos-x').value;
  const yInput = document.getElementById('datos-y').value;
  const ecuacion = document.getElementById('ecuacion-recta');
  const xPrediccion = document.getElementById('x-prediccion');
  const resultadoPred = document.getElementById('resultado-prediccion');

  const x = parseNumbers(xInput);
  const y = parseNumbers(yInput);

  if (x.length !== y.length || x.length === 0) {
    ecuacion.textContent = 'Error: X e Y deben tener igual longitud.';
    return;
  }

  const n = x.length;
  const sumX = x.reduce((a, b) => a + b, 0);
  const sumY = y.reduce((a, b) => a + b, 0);
  const sumXY = x.reduce((sum, xi, i) => sum + xi * y[i], 0);
  const sumX2 = x.reduce((sum, xi) => sum + xi * xi, 0);

  b = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
  a = (sumY - b * sumX) / n;

  ecuacion.textContent = `y = ${a.toFixed(4)} + ${b.toFixed(4)}x`;
  resultadoPred.textContent = 'Y ≈ ---';
  xPrediccion.value = '';

  graficarRegresion(x, y, a, b);
}

function predecirValorY() {
  const xVal = parseFloat(document.getElementById('x-prediccion').value);
  const salida = document.getElementById('resultado-prediccion');

  if (!isNaN(xVal)) {
    const yPred = a + b * xVal;
    salida.textContent = `Y ≈ ${yPred.toFixed(4)}`;
  } else {
    salida.textContent = 'Y ≈ ---';
  }
}

function graficarRegresion(x, y, a, b) {
  const puntos = x.map((xi, i) => ({ x: xi, y: y[i] }));
  const minX = Math.min(...x);
  const maxX = Math.max(...x);
  const lineaRegresion = [
    { x: minX, y: a + b * minX },
    { x: maxX, y: a + b * maxX }
  ];

  const ctx = document.getElementById('grafica-cuadrados').getContext('2d');
  if (chartCuadrados) {
    chartCuadrados.destroy();
  }

  chartCuadrados = new Chart(ctx, {
    type: 'scatter',
    data: {
      datasets: [
        {
          label: 'Datos',
          data: puntos,
          backgroundColor: 'blue'
        },
        {
          label: 'Línea de regresión',
          type: 'line',
          data: lineaRegresion,
          borderColor: 'red',
          borderWidth: 2,
          fill: false,
          tension: 0
        }
      ]
    },
    options: {
      scales: {
        x: {
          title: { display: true, text: 'X' }
        },
        y: {
          title: { display: true, text: 'Y' }
        }
      }
    }
  });
}

async function downloadChart(type) {
    const canvas = document.getElementById("grafica-cuadrados");
    const container = canvas.parentNode;

    // Usa html2canvas para capturar el canvas
    const canvasImage = await html2canvas(container);

    if (type === "png") {
      const link = document.createElement("a");
      link.download = "grafica.png";
      link.href = canvasImage.toDataURL("image/png");
      link.click();
    } else if (type === "pdf") {
      const { jsPDF } = window.jspdf;
      const pdf = new jsPDF();
      const imgData = canvasImage.toDataURL("image/png");

      const imgProps = pdf.getImageProperties(imgData);
      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;

      pdf.addImage(imgData, "PNG", 0, 0, pdfWidth, pdfHeight);
      pdf.save("grafica.pdf");
    }
  }

let graficaDescriptiva = null;

function calcularDescriptiva() {
  const input = document.getElementById("datos-desc").value;
  const datos = input.split(/[\s,]+/).map(Number).filter(x => !isNaN(x));

  if (datos.length === 0) {
    document.getElementById("resultado-desc").textContent = "Por favor, ingresa datos válidos.";
    return;
  }

  const n = datos.length;
  const media = datos.reduce((a, b) => a + b, 0) / n;
  const varianza = datos.reduce((acc, val) => acc + Math.pow(val - media, 2), 0) / n;
  const desviacion = Math.sqrt(varianza);
  const min = Math.min(...datos);
  const max = Math.max(...datos);

  const resultado = `
Cantidad de datos: ${n}
Media: ${media.toFixed(2)}
Varianza: ${varianza.toFixed(2)}
Desviación estándar: ${desviacion.toFixed(2)}
Mínimo: ${min}
Máximo: ${max}
  `;
  document.getElementById("resultado-desc").textContent = resultado.trim();

  // === Preparar datos para la gráfica ===
  const etiquetas = [
    "Cantidad de datos",
    "Media",
    "Varianza",
    "Desviación estándar",
    "Mínimo",
    "Máximo"
  ];
  const valores = [n, media, varianza, desviacion, min, max];

  const ctx = document.getElementById("grafica-descriptiva").getContext("2d");

  // Destruir gráfica anterior si existe
  if (graficaDescriptiva !== null) {
    graficaDescriptiva.destroy();
  }

  graficaDescriptiva = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: etiquetas,
      datasets: [{
        label: 'Valor',
        data: valores,
        backgroundColor: [
          'rgba(255, 99, 132, 0.6)',
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 206, 86, 0.6)',
          'rgba(75, 192, 192, 0.6)',
          'rgba(153, 102, 255, 0.6)',
          'rgba(255, 159, 64, 0.6)'
        ],
        borderColor: 'rgba(0,0,0,0.1)',
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      plugins: {
        tooltip: {
          enabled: true
        },
        legend: {
          display: false
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            stepSize: 1
          },
          title: {
            display: true,
            text: 'Valor'
          }
        }
      }
    }
  });
}

