import csv
import graphviz
import os

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
        self.raiz = self._insertar_recursivo(self.raiz, valor)
    
    def _insertar_recursivo(self, nodo, valor):
        if nodo is None:
            return Nodo(valor)
        if valor < nodo.valor:
            nodo.izquierda = self._insertar_recursivo(nodo.izquierda, valor)
        elif valor > nodo.valor:
            nodo.derecha = self._insertar_recursivo(nodo.derecha, valor)
        
        nodo.altura = 1 + max(self._obtener_altura(nodo.izquierda), self._obtener_altura(nodo.derecha))
        return self._balancear(nodo)

    def _obtener_altura(self, nodo):
        return nodo.altura if nodo else 0

    def _obtener_balance(self, nodo):
        return self._obtener_altura(nodo.izquierda) - self._obtener_altura(nodo.derecha) if nodo else 0

    def _balancear(self, nodo):
        balance = self._obtener_balance(nodo)
        if balance > 1:
            if self._obtener_balance(nodo.izquierda) < 0:
                nodo.izquierda = self._rotacion_izquierda(nodo.izquierda)
            return self._rotacion_derecha(nodo)
        if balance < -1:
            if self._obtener_balance(nodo.derecha) > 0:
                nodo.derecha = self._rotacion_derecha(nodo.derecha)
            return self._rotacion_izquierda(nodo)
        return nodo

    def _rotacion_izquierda(self, z):
        y = z.derecha
        T2 = y.izquierda
        y.izquierda = z
        z.derecha = T2
        z.altura = 1 + max(self._obtener_altura(z.izquierda), self._obtener_altura(z.derecha))
        y.altura = 1 + max(self._obtener_altura(y.izquierda), self._obtener_altura(y.derecha))
        return y

    def _rotacion_derecha(self, z):
        y = z.izquierda
        T3 = y.derecha
        y.derecha = z
        z.izquierda = T3
        z.altura = 1 + max(self._obtener_altura(z.izquierda), self._obtener_altura(z.derecha))
        y.altura = 1 + max(self._obtener_altura(y.izquierda), self._obtener_altura(y.derecha))
        return y

    def buscar(self, valor):
        return self._buscar_recursivo(self.raiz, valor)

    def _buscar_recursivo(self, nodo, valor):
        if nodo is None or nodo.valor == valor:
            return nodo
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
            
            sucesor = self._obtener_minimo(nodo.derecha)
            nodo.valor = sucesor.valor
            nodo.derecha = self._eliminar_recursivo(nodo.derecha, sucesor.valor)
        
        return self._balancear(nodo)

    def _obtener_minimo(self, nodo):
        while nodo.izquierda:
            nodo = nodo.izquierda
        return nodo

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

    def generar_graphviz(self):
        if self.raiz is None:
            print("El árbol está vacío.")
            return
        
        dot = graphviz.Digraph(format='png')
        self._agregar_nodos(dot, self.raiz)
        
        try:
            escritorio = os.path.join(os.path.expanduser("~"), "Desktop")
            ruta_salida = os.path.join(escritorio, "arbol_avl")
            dot.render(ruta_salida)
            os.system(f'start {ruta_salida}.png')
        except Exception as e:
            print(f"Error al generar la imagen: {e}")

    def _agregar_nodos(self, dot, nodo):
        if nodo:
            dot.node(str(nodo.valor))
            if nodo.izquierda:
                dot.edge(str(nodo.valor), str(nodo.izquierda.valor))
                self._agregar_nodos(dot, nodo.izquierda)
            if nodo.derecha:
                dot.edge(str(nodo.valor), str(nodo.derecha.valor))
                self._agregar_nodos(dot, nodo.derecha)

def menu():
    arbol = ArbolAVL()
    
    while True:
        print("\nMenú - Árbol AVL")
        print("1. Insertar número")
        print("2. Buscar número")
        print("3. Eliminar número")
        print("4. Cargar desde CSV")
        print("5. Visualizar con Graphviz")
        print("6. Salir")
        
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            valor = int(input("Ingrese el número a insertar: "))
            arbol.insertar(valor)
            print(f"Número {valor} insertado en el árbol.")
            input("Presione Enter para continuar...")
        elif opcion == "2":
            valor = int(input("Ingrese el número a buscar: "))
            print("Número encontrado" if arbol.buscar(valor) else "Número no encontrado")
            input("Presione Enter para continuar...")
        elif opcion == "3":
            valor = int(input("Ingrese el número a eliminar: "))
            arbol.eliminar(valor)
            print(f"Número {valor} eliminado del árbol.")
            input("Presione Enter para continuar...")
        elif opcion == "4":
            ruta = input("Ingrese la ruta del archivo CSV: ")
            arbol.cargar_desde_csv(ruta)
            input("Presione Enter para continuar...")
        elif opcion == "5":
            arbol.generar_graphviz()
            print("Se ha generado la representación visual del árbol.")
            input("Presione Enter para continuar...")
        elif opcion == "6":
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu()
