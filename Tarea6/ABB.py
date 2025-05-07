import csv
import time
import matplotlib.pyplot as plt
import pandas as pd
import os
import graphviz

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None

class ArbolBinario:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        if self.raiz is None:
            self.raiz = Nodo(valor)
        else:
            self._insertar_recursivo(self.raiz, valor)

    def _insertar_recursivo(self, nodo, valor):
        if valor < nodo.valor:
            if nodo.izquierda is None:
                nodo.izquierda = Nodo(valor)
            else:
                self._insertar_recursivo(nodo.izquierda, valor)
        elif valor > nodo.valor:
            if nodo.derecha is None:
                nodo.derecha = Nodo(valor)
            else:
                self._insertar_recursivo(nodo.derecha, valor)

    def buscar(self, valor):
        return self._buscar_recursivo(self.raiz, valor)

    def _buscar_recursivo(self, nodo, valor):
        if nodo is None:
            return False
        if nodo.valor == valor:
            return True
        if valor < nodo.valor:
            return self._buscar_recursivo(nodo.izquierda, valor)
        return self._buscar_recursivo(nodo.derecha, valor)

    def eliminar(self, valor):
        self.raiz = self._eliminar_recursivo(self.raiz, valor)

    def _eliminar_recursivo(self, nodo, valor):
        if nodo is None:
            return nodo
        if valor < nodo.valor:
            nodo.izquierda = self._eliminar_recursivo(nodo.izquierda, valor)
        elif valor > nodo.valor:
            nodo.derecha = self._eliminar_recursivo(nodo.derecha, valor)
        else:
            if nodo.izquierda is None:
                return nodo.derecha
            elif nodo.derecha is None:
                return nodo.izquierda
            sucesor = self._minimo_valor_nodo(nodo.derecha)
            nodo.valor = sucesor.valor
            nodo.derecha = self._eliminar_recursivo(nodo.derecha, sucesor.valor)
        return nodo

    def _minimo_valor_nodo(self, nodo):
        actual = nodo
        while actual.izquierda is not None:
            actual = actual.izquierda
        return actual

def analisis_empirico(ruta_csv):
    print("Cargando CSV...")
    df = pd.read_csv(ruta_csv)
    print("Columnas disponibles:")
    print(df.columns.tolist())
    columna = input("Selecciona el nombre de la columna numérica para trabajar: ")

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

    arbol = ArbolBinario()

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
    plt.title(f"Tiempos con {cantidad} datos - Árbol Binario de Búsqueda")
    plt.ylabel("Tiempo (segundos)")
    plt.savefig("tiempos_abb.png")
    print("Gráfico guardado como tiempos_abb.png")

if __name__ == "__main__":
    ruta = input("Ingrese la ruta del archivo CSV: ")
    analisis_empirico(ruta)
