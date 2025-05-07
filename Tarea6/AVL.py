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
        self.altura = 1

class ArbolAVL:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        self.raiz = self._insertar(self.raiz, valor)

    def _insertar(self, nodo, valor):
        if nodo is None:
            return Nodo(valor)
        if valor < nodo.valor:
            nodo.izquierda = self._insertar(nodo.izquierda, valor)
        elif valor > nodo.valor:
            nodo.derecha = self._insertar(nodo.derecha, valor)
        else:
            return nodo  # Duplicado, no se inserta

        nodo.altura = 1 + max(self._altura(nodo.izquierda), self._altura(nodo.derecha))
        return self._balancear(nodo)

    def _altura(self, nodo):
        return nodo.altura if nodo else 0

    def _balance(self, nodo):
        return self._altura(nodo.izquierda) - self._altura(nodo.derecha) if nodo else 0

    def _rotacion_izquierda(self, z):
        y = z.derecha
        T2 = y.izquierda
        y.izquierda = z
        z.derecha = T2
        z.altura = 1 + max(self._altura(z.izquierda), self._altura(z.derecha))
        y.altura = 1 + max(self._altura(y.izquierda), self._altura(y.derecha))
        return y

    def _rotacion_derecha(self, z):
        y = z.izquierda
        T3 = y.derecha
        y.derecha = z
        z.izquierda = T3
        z.altura = 1 + max(self._altura(z.izquierda), self._altura(z.derecha))
        y.altura = 1 + max(self._altura(y.izquierda), self._altura(y.derecha))
        return y

    def _balancear(self, nodo):
        balance = self._balance(nodo)
        if balance > 1:
            if self._balance(nodo.izquierda) < 0:
                nodo.izquierda = self._rotacion_izquierda(nodo.izquierda)
            return self._rotacion_derecha(nodo)
        if balance < -1:
            if self._balance(nodo.derecha) > 0:
                nodo.derecha = self._rotacion_derecha(nodo.derecha)
            return self._rotacion_izquierda(nodo)
        return nodo

    def buscar(self, valor):
        return self._buscar_recursivo(self.raiz, valor)

    def _buscar_recursivo(self, nodo, valor):
        if nodo is None:
            return False
        if valor == nodo.valor:
            return True
        elif valor < nodo.valor:
            return self._buscar_recursivo(nodo.izquierda, valor)
        else:
            return self._buscar_recursivo(nodo.derecha, valor)

    def eliminar(self, valor):
        self.raiz = self._eliminar(self.raiz, valor)

    def _eliminar(self, nodo, valor):
        if nodo is None:
            return nodo
        if valor < nodo.valor:
            nodo.izquierda = self._eliminar(nodo.izquierda, valor)
        elif valor > nodo.valor:
            nodo.derecha = self._eliminar(nodo.derecha, valor)
        else:
            if nodo.izquierda is None:
                return nodo.derecha
            elif nodo.derecha is None:
                return nodo.izquierda
            sucesor = self._minimo(nodo.derecha)
            nodo.valor = sucesor.valor
            nodo.derecha = self._eliminar(nodo.derecha, sucesor.valor)

        nodo.altura = 1 + max(self._altura(nodo.izquierda), self._altura(nodo.derecha))
        return self._balancear(nodo)

    def _minimo(self, nodo):
        while nodo.izquierda:
            nodo = nodo.izquierda
        return nodo

def analisis_empirico_avl(ruta_csv):
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

    arbol = ArbolAVL()

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
    plt.title(f"Tiempos con {cantidad} datos - Árbol AVL")
    plt.ylabel("Tiempo (segundos)")
    plt.savefig("tiempos_avl.png")
    print("Gráfico guardado como tiempos_avl.png")

if __name__ == "__main__":
    ruta = input("Ingrese la ruta del archivo CSV: ")
    analisis_empirico_avl(ruta)
