import graphviz
import os

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

    def cargar_desde_archivo(self, ruta):
        try:
            with open(ruta, "r") as archivo:
                for linea in archivo:
                    try:
                        valor = int(linea.strip())
                        self.insertar(valor)
                    except ValueError:
                        print(f"Valor inválido en el archivo: {linea.strip()}")
        except FileNotFoundError:
            print("Archivo no encontrado.")

    def generar_graphviz(self):
        if self.raiz is None:
            print("El árbol está vacío.")
            return
        
        dot = graphviz.Digraph(format='png')
        self._agregar_nodos(dot, self.raiz)

        try:
            escritorio = os.path.join(os.path.expanduser("~"), "Desktop")
            ruta_salida = os.path.join(escritorio, "arbol_binario")
            dot.render(ruta_salida)
            ruta_completa = ruta_salida + ".png"
            print(f"Imagen generada en: {ruta_completa}")
            os.system(f'start {ruta_completa}')
        except Exception as e:
            print(f"Error al generar la imagen: {e}")

    def _agregar_nodos(self, dot, nodo):
        if nodo is not None:
            dot.node(str(nodo.valor))
            if nodo.izquierda is not None:
                dot.edge(str(nodo.valor), str(nodo.izquierda.valor))
                self._agregar_nodos(dot, nodo.izquierda)
            if nodo.derecha is not None:
                dot.edge(str(nodo.valor), str(nodo.derecha.valor))
                self._agregar_nodos(dot, nodo.derecha)

def menu():
    arbol = ArbolBinario()

    while True:
        print("\nMenú - Árbol Binario de Búsqueda")
        print("1. Insertar número")
        print("2. Buscar número")
        print("3. Eliminar número")
        print("4. Cargar desde archivo")
        print("5. Mostrar árbol en Graphviz")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            valor = int(input("Ingrese el número a insertar: "))
            arbol.insertar(valor)
            print(f"Número {valor} insertado en el árbol.")
            input("Presione Enter para continuar...")

        elif opcion == "2":
            valor = int(input("Ingrese el número a buscar: "))
            if arbol.buscar(valor):
                print(f"El número {valor} está en el árbol.")
            else:
                print(f"El número {valor} no se encuentra en el árbol.")
            input("Presione Enter para continuar...")

        elif opcion == "3":
            valor = int(input("Ingrese el número a eliminar: "))
            arbol.eliminar(valor)
            print(f"Número {valor} eliminado del árbol.")
            input("Presione Enter para continuar...")

        elif opcion == "4":
            ruta = input("Ingrese la ruta del archivo: ")
            arbol.cargar_desde_archivo(ruta)
            print("Datos cargados desde el archivo.")
            input("Presione Enter para continuar...")

        elif opcion == "5":
            arbol.generar_graphviz()
            print("Se ha generado la representación visual del árbol.")
            input("Presione Enter para continuar...")

        elif opcion == "6":
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida, intente de nuevo.")

if __name__ == "__main__":
    menu()
