import csv
import graphviz
import os
import math
from graphviz import Digraph, nohtml

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

    def buscar(self, k, nodo=None):
        if nodo is None:
            nodo = self.raiz
        i = 0
        while i < len(nodo.claves) and k > nodo.claves[i]:
            i += 1
        if i < len(nodo.claves) and nodo.claves[i] == k:
            return True
        if nodo.hoja:
            return False
        return self.buscar(k, nodo.hijos[i])

    def insertar(self, k):
        r = self.raiz
        if len(r.claves) == self.max_claves:
            self._insertar_no_lleno(r, k)
            if len(r.claves) > self.max_claves:
                s = NodoB(self.grado, False)
                s.hijos.append(r)
                self._dividir_hijo(s, 0)
                self.raiz = s
        else:
            self._insertar_no_lleno(r, k)

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
        grado = self.grado
        y = padre.hijos[i]
        z = NodoB(grado, y.hoja)
        medio = (self.grado - 1) // 2

        padre.claves.insert(i, y.claves[medio])
        padre.hijos.insert(i + 1, z)

        z.claves = y.claves[medio + 1:]
        y.claves = y.claves[:medio]

        if not y.hoja:
            z.hijos = y.hijos[medio + 1:]
            y.hijos = y.hijos[:medio + 1]

    def eliminar(self, k):
        print("La eliminación aún no ha sido implementada.")

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

    def graficar(self, nombre_archivo="arbol_b"):
        dot = Digraph('BTree', filename=nombre_archivo,
                      node_attr={'shape': 'record', 'height': '.1'})
        self._graficar_nodo(self.raiz, dot)

        try:
            escritorio = os.path.join(os.path.expanduser("~"), "Desktop")
            ruta_salida = os.path.join(escritorio, nombre_archivo)
            dot.render(ruta_salida, cleanup=True, format='png')
            os.startfile(f"{ruta_salida}.png")  
        except Exception as e:
            print(f"Error al generar o abrir la imagen: {e}")

    def _graficar_nodo(self, nodo, dot):
        id_actual = f'node{id(nodo)}'
        etiquetas = []

        for i, clave in enumerate(nodo.claves):
            etiquetas.append(f'<f{i+1}>{clave}')
        etiquetas.insert(0, '<f0>')
        etiquetas.append(f'<f{len(nodo.claves)+1}>')

        etiqueta_final = '|'.join(etiquetas)
        dot.node(id_actual, nohtml(etiqueta_final))

        for i, hijo in enumerate(nodo.hijos):
            id_hijo = f'node{id(hijo)}'
            self._graficar_nodo(hijo, dot)
            dot.edge(f'{id_actual}:f{i}', f'{id_hijo}:f1')

# --- CONFIGURACIÓN INICIAL ---
def configurar_arbol():
    while True:
        try:
            grado = int(input("Ingrese el grado del Árbol B (mínimo 2): "))
            if grado >= 2:
                print(f"\n Árbol B configurado:")
                print(f"- Grado del árbol: {grado}")
                print(f"- Máximo de claves por nodo: {grado - 1}")
                print(f"- Mínimo de claves por nodo: {math.ceil((grado + 1) / 2) - 1}")
                if grado % 2 == 0:
                    print("🔷 Método usado: Agregar → Dividir (grado PAR)")
                else:
                    print("🔶 Método usado: Dividir → Agregar (grado IMPAR)")
                return ArbolB(grado)
            else:
                print("El grado debe ser al menos 2.")
        except ValueError:
            print("Por favor, ingrese un número entero válido.")


# --- MENÚ PRINCIPAL ---
def menu():
    print("=== Configuración Inicial del Árbol B ===")
    arbol = configurar_arbol()

    while True:
        print("\nMenú - Árbol B")
        print("1. Insertar número")
        print("2. Buscar número")
        print("3. Eliminar número")
        print("4. Cargar desde CSV")
        print("5. Visualizar con Graphviz")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            try:
                valor = int(input("Ingrese el número a insertar: "))
                arbol.insertar(valor)
                print(f"Número {valor} insertado en el árbol.")
            except ValueError:
                print("Entrada inválida.")
            input("Presione Enter para continuar...")

        elif opcion == "2":
            try:
                valor = int(input("Ingrese el número a buscar: "))
                print("Número encontrado" if arbol.buscar(valor) else "Número no encontrado")
            except ValueError:
                print("Entrada inválida.")
            input("Presione Enter para continuar...")

        elif opcion == "3":
            input("Presione Enter para continuar...")

        elif opcion == "4":
            ruta = input("Ingrese la ruta del archivo CSV: ")
            arbol.cargar_desde_csv(ruta)
            input("Presione Enter para continuar...")

        elif opcion == "5":
            arbol.graficar()
            print("Se ha generado la representación visual del árbol.")
            input("Presione Enter para continuar...")

        elif opcion == "6":
            print("Programa finalizado.")
            break

        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu()