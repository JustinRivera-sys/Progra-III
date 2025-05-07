import csv
import time
import matplotlib.pyplot as plt
import pandas as pd
import math

class NodoB:
    def __init__(self, grado, hoja=False):
        self.grado = grado
        self.hoja = hoja
        self.claves = []
        self.hijos = []

class ArbolB:
    def __init__(self, grado):
        self.grado = grado
        self.raiz = NodoB(grado, True)
        self.max_claves = grado - 1
        self.min_claves = math.ceil((grado + 1) / 2) - 1

    def insertar(self, k):
        r = self.raiz
        if len(r.claves) == self.max_claves:
            s = NodoB(self.grado, False)
            s.hijos.append(self.raiz)
            self._dividir_hijo(s, 0)
            self.raiz = s
        self._insertar_no_lleno(self.raiz, k)

    def _insertar_no_lleno(self, nodo, k):
        i = len(nodo.claves) - 1
        if nodo.hoja:
            nodo.claves.append(None)
            while i >= 0 and k < nodo.claves[i]:
                nodo.claves[i + 1] = nodo.claves[i]
                i -= 1
            nodo.claves[i + 1] = k
        else:
            while i >= 0 and k < nodo.claves[i]:
                i -= 1
            i += 1
            self._insertar_no_lleno(nodo.hijos[i], k)
            if len(nodo.hijos[i].claves) > self.max_claves:
                self._dividir_hijo(nodo, i)

    def _dividir_hijo(self, padre, i):
        y = padre.hijos[i]
        z = NodoB(self.grado, y.hoja)
        medio = (self.grado - 1) // 2
        padre.claves.insert(i, y.claves[medio])
        padre.hijos.insert(i + 1, z)
        z.claves = y.claves[medio + 1:]
        y.claves = y.claves[:medio]

        if not y.hoja:
            z.hijos = y.hijos[medio + 1:]
            y.hijos = y.hijos[:medio + 1]

    def buscar(self, k):
        return self._buscar(self.raiz, k)

    def _buscar(self, nodo, k):
        i = 0
        while i < len(nodo.claves) and k > nodo.claves[i]:
            i += 1
        if i < len(nodo.claves) and nodo.claves[i] == k:
            return True
        if nodo.hoja:
            return False
        return self._buscar(nodo.hijos[i], k)

    def eliminar(self, k):
        print("La eliminación no está implementada aún.")

    def cargar_desde_csv(self, ruta):
        try:
            with open(ruta, "r") as archivo:
                lector = csv.reader(archivo)
                for fila in lector:
                    for valor in fila:
                        try:
                            self.insertar(int(valor.strip()))
                        except ValueError:
                            print(f"Valor inválido en el archivo: {valor.strip()}")
            print("Carga completada.")
        except FileNotFoundError:
            print("Archivo no encontrado.")

def analisis_empirico(ruta_csv):
    print("Cargando CSV...")
    df = pd.read_csv(ruta_csv)
    print("Columnas disponibles:")
    print(df.columns.tolist())
    columna = input("Selecciona la columna numérica para trabajar: ")

    datos = df[columna].dropna()

    try:
        datos = datos.astype(int).tolist()
    except:
        print("No se puede convertir la columna a números enteros.")
        return

    total_datos = len(datos)
    print(f"\nCantidad total de datos disponibles: {total_datos}")
    cantidad = input("¿Cuántos datos desea analizar? (Presione Enter para usar todos): ")

    if cantidad.strip().isdigit():
        cantidad = int(cantidad)
        if cantidad > total_datos:
            print("Se usarán todos los datos disponibles.")
            cantidad = total_datos
    else:
        cantidad = total_datos

    datos = datos[:cantidad]

    grado = int(input("Ingrese el grado del Árbol B (mínimo 2): "))
    arbol = ArbolB(grado)

    # Medición de inserción
    inicio = time.time()
    for valor in datos:
        arbol.insertar(valor)
    fin = time.time()
    tiempo_insercion = fin - inicio

    # Medición de búsqueda
    inicio = time.time()
    for valor in datos:
        arbol.buscar(valor)
    fin = time.time()
    tiempo_busqueda = fin - inicio

    # Medición de eliminación
    inicio = time.time()
    for valor in datos:
        arbol.eliminar(valor)
    fin = time.time()
    tiempo_eliminacion = fin - inicio

    print("\n--- Resultados ---")
    print(f"Datos analizados: {cantidad}")
    print(f"Inserción: {tiempo_insercion:.6f} segundos")
    print(f"Búsqueda: {tiempo_busqueda:.6f} segundos")
    print(f"Eliminación: {tiempo_eliminacion:.6f} segundos")

    # Gráfico
    operaciones = ["Inserción", "Búsqueda", "Eliminación"]
    tiempos = [tiempo_insercion, tiempo_busqueda, tiempo_eliminacion]

    plt.figure(figsize=(8, 5))
    plt.bar(operaciones, tiempos, color=['green', 'blue', 'red'])
    plt.title(f"Tiempos con {cantidad} datos - Árbol B")
    plt.ylabel("Tiempo (segundos)")
    plt.savefig("tiempos_arbol_b.png")
    print("Gráfico guardado como tiempos_arbol_b.png")

if __name__ == "__main__":
    ruta = input("Ingrese la ruta del archivo CSV: ")
    analisis_empirico(ruta)
