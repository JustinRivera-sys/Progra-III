import os
from graphviz import Digraph


class Nodo:
    def __init__(self, nombre, apellido, carnet):
        self.nombre = nombre
        self.apellido = apellido
        self.carnet = carnet
        self.siguiente = None
        self.anterior = None

class ListaDoblementeEnlazada:
    def __init__(self):
        self.cabeza = None
        self.cola = None
    
    def insertar_al_principio(self, nombre, apellido, carnet):
        nuevo_nodo = Nodo(nombre, apellido, carnet)
        if not self.cabeza:
            self.cabeza = self.cola = nuevo_nodo
        else:
            nuevo_nodo.siguiente = self.cabeza
            self.cabeza.anterior = nuevo_nodo
            self.cabeza = nuevo_nodo

    def insertar_al_final(self, nombre, apellido, carnet):
        nuevo_nodo = Nodo(nombre, apellido, carnet)
        if not self.cola:
            self.cabeza = self.cola = nuevo_nodo
        else:
            nuevo_nodo.anterior = self.cola
            self.cola.siguiente = nuevo_nodo
            self.cola = nuevo_nodo

    def eliminar_por_valor(self, carnet):
        actual = self.cabeza
        while actual:
            if actual.carnet == carnet:
                if actual.anterior:
                    actual.anterior.siguiente = actual.siguiente
                else:
                    self.cabeza = actual.siguiente
                
                if actual.siguiente:
                    actual.siguiente.anterior = actual.anterior
                else:
                    self.cola = actual.anterior
                
                del actual
                print("Nodo eliminado.")
                return
            actual = actual.siguiente
        print("Nodo no encontrado.")
    
    def mostrar_lista(self):
        actual = self.cabeza
        elementos = []
        while actual:
            elementos.append(f"[{actual.nombre} {actual.apellido}, {actual.carnet}]")
            actual = actual.siguiente
        print(" <-> ".join(elementos) if elementos else "Lista vacía")

    def generar_grafico(self):
        """Genera un gráfico de la lista enlazada usando Graphviz"""
        if not self.cabeza:
            print("La lista está vacía, no se puede generar el gráfico.")
            return

        dot = Digraph(comment='Lista Doblemente Enlazada', format="png")

        actual = self.cabeza
        while actual:
            label = f"{actual.nombre} {actual.apellido}\n{actual.carnet}"
            dot.node(str(id(actual)), label=label, shape="box")

            if actual.siguiente:
                dot.edge(str(id(actual)), str(id(actual.siguiente)), constraint="true")
                dot.edge(str(id(actual.siguiente)), str(id(actual)), constraint="true")  # Flecha bidireccional

            actual = actual.siguiente

        output_path = dot.render('lista_doble')
        print(f"Gráfico generado: {output_path}")

# Interfaz de Línea de Comandos
def menu():
    lista = ListaDoblementeEnlazada()
    while True:
        print("\nMenú de opciones:")
        print("1. Insertar al principio")
        print("2. Insertar al final")
        print("3. Eliminar por carnet")
        print("4. Mostrar lista")
        print("5. Generar gráfico")
        print("6. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            nombre = input("Ingrese el nombre: ")
            apellido = input("Ingrese el apellido: ")
            carnet = input("Ingrese el carnet: ")
            lista.insertar_al_principio(nombre, apellido, carnet)
        elif opcion == "2":
            nombre = input("Ingrese el nombre: ")
            apellido = input("Ingrese el apellido: ")
            carnet = input("Ingrese el carnet: ")
            lista.insertar_al_final(nombre, apellido, carnet)
        elif opcion == "3":
            carnet = input("Ingrese el carnet a eliminar: ")
            lista.eliminar_por_valor(carnet)
        elif opcion == "4":
            lista.mostrar_lista()
        elif opcion == "5":
            lista.generar_grafico()
        elif opcion == "6":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida, intente de nuevo.")

if __name__ == "__main__":
    menu()
