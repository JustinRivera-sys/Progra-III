import csv
import time
import random
import matplotlib.pyplot as plt


class Nodo:
    def __init__(self, vin, make, model):
        self.vin = vin
        self.make = make
        self.model = model
        self.siguiente = None


class ListaSimple:
    def __init__(self):
        self.cabeza = None

    def insertar_al_final(self, vin, make, model):
        nuevo = Nodo(vin, make, model)
        if not self.cabeza:
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo

    def buscar(self, vin):
        actual = self.cabeza
        while actual:
            if actual.vin == vin:
                return actual
            actual = actual.siguiente
        return None

    def eliminar_por_vin(self, vin):
        actual = self.cabeza
        anterior = None
        while actual:
            if actual.vin == vin:
                if anterior:
                    anterior.siguiente = actual.siguiente
                else:
                    self.cabeza = actual.siguiente
                return True
            anterior = actual
            actual = actual.siguiente
        return False

    def cargar_desde_csv(self, ruta_csv, limite=None):
        datos = []
        with open(ruta_csv, newline='', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for i, fila in enumerate(lector):
                if limite and i >= limite:
                    break
                vin = fila.get("VIN (1-10)")
                make = fila.get("Make")
                model = fila.get("Model")
                if vin and make and model:
                    datos.append((vin.strip(), make.strip(), model.strip()))
        return datos

    def medir_insercion(self, datos):
        inicio = time.perf_counter()
        for vin, make, model in datos:
            self.insertar_al_final(vin, make, model)
        fin = time.perf_counter()
        return fin - inicio

    def medir_busqueda(self, vins):
        inicio = time.perf_counter()
        for vin in vins:
            self.buscar(vin)
        fin = time.perf_counter()
        return fin - inicio

    def medir_eliminacion(self, vins):
        inicio = time.perf_counter()
        for vin in vins:
            self.eliminar_por_vin(vin)
        fin = time.perf_counter()
        return fin - inicio


def graficar(tiempos):
    operaciones = ["Inserción", "Búsqueda", "Eliminación"]
    plt.figure(figsize=(8, 5))
    plt.bar(operaciones, tiempos, color=["green", "blue", "red"])
    plt.title("Tiempos de operaciones en Lista Simple")
    plt.ylabel("Tiempo (segundos)")
    plt.savefig("grafico_lista_simple.png")
    print("Gráfico guardado como grafico_lista_simple.png")


if __name__ == "__main__":
    ruta = input("Ingrese la ruta del archivo CSV: ").strip()
    limite = input("¿Cuántos registros desea cargar (presione Enter para todos)?: ").strip()
    limite = int(limite) if limite.isdigit() else None

    lista = ListaSimple()
    try:
        datos = lista.cargar_desde_csv(ruta, limite)
        if not datos:
            print("No se encontraron datos válidos en el CSV.")
            exit()

        print(f"\nCargando {len(datos)} registros...")

        tiempo_insercion = lista.medir_insercion(datos)
        muestras = min(100, len(datos))
        vins_para_test = random.sample([vin for vin, _, _ in datos], muestras)
        tiempo_busqueda = lista.medir_busqueda(vins_para_test)
        tiempo_eliminacion = lista.medir_eliminacion(vins_para_test)

        print("\n--- Resultados del experimento con Lista Simple ---")
        print(f"Inserción de {len(datos)} elementos: {tiempo_insercion:.6f} segundos")
        print(f"Búsqueda de {muestras} elementos: {tiempo_busqueda:.6f} segundos")
        print(f"Eliminación de {muestras} elementos: {tiempo_eliminacion:.6f} segundos")

        graficar([tiempo_insercion, tiempo_busqueda, tiempo_eliminacion])

    except FileNotFoundError:
        print("No se encontró el archivo. Verifique la ruta e intente nuevamente.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")
