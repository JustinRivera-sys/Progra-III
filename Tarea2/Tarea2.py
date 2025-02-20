import os

#CONVERTIR A BINARIO
def convertir_a_binario(n):
    if n == 0:
        return "0"
    elif n == 1:
        return "1"
    else:
        return convertir_a_binario(n // 2) + str(n % 2)

#CONTAR DIGITOS
def contar_digitos(n):
    if n == 0:
        return 0
    else:
        return 1 + contar_digitos(n // 10)

#RAIZ CUADRADA ENTERA
# Función secundaria de la raiz
def calcular_raiz_cuadrada(numero, intento=0):
    if intento * intento > numero:
        return intento - 1
    elif intento * intento == numero:
        return intento
    else:
        return calcular_raiz_cuadrada(numero, intento + 1)

# Función principal que valida el número e invoca la función recursiva
def raiz_cuadrada_entera(numero):
    if numero < 0:
        print("El número debe ser no negativo.")
        return None
    return calcular_raiz_cuadrada(numero)


# ROMANOS A DECIMAL
def convertir_a_decimal(romano):
    # El diccionario de valores romanos debe estar indentado
    valores_romanos = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000
    }
    if len(romano) == 0:
        return 0
    valor_actual = valores_romanos[romano[0]]
    if len(romano) == 1 or valor_actual >= valores_romanos[romano[1]]:
        return valor_actual + convertir_a_decimal(romano[1:])  
    else:
        return -valor_actual + convertir_a_decimal(romano[1:])  


#SUMA DE NUMEROS ENTEROS 
def suma_numeros_enteros(n):
    if n == 0:
        return 0
    else:
        return n + suma_numeros_enteros(n - 1)



# Interfaz de MENU
def menu():

    while True:
        print("\nMenú de opciones:")
        print("1. Convertir a Binario")
        print("2. Contar Dígitos")
        print("3. Raíz Cuadrada Entera")
        print("4. Convertir a Decimal desde Romano")
        print("5. Suma de Números Entero")
        print("6. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            numero = int(input("Ingrese el número: "))  # Convertir a entero
            resultado = convertir_a_binario(numero)# Metodo para convertir a binario
            print(f"Tu número es: {numero} y en Binario es: {resultado}")  # Imprimir el número ingresado
            input("Presiona Enter para salir al menu principal...") 
        
        elif opcion == "2":
            numero = int(input("Ingrese un número entero: "))
            resultado = contar_digitos(abs(numero))  # Usamos abs() para manejar números negativos
            print(f"El número {numero} tiene {resultado} dígitos.")
            input("Presiona Enter para continuar...")


        elif opcion == "3":
            numero = int(input("Ingrese un número entero no negativo: "))
            resultado = raiz_cuadrada_entera(numero)
            if resultado is not None:
                    print(f"La raíz cuadrada entera de {numero} es: {resultado}")
            input("Presiona Enter para continuar...")


        elif opcion == "4":
            numero_romano = input("Ingrese un número romano: ").upper()
            resultado = convertir_a_decimal(numero_romano)
            print(f"El número romano {numero_romano} es equivalente a {resultado} en decimal.")
            input("Presiona Enter para continuar...")


        elif opcion == "5":
            numero = int(input("Ingrese un número entero positivo: "))
            if numero < 0:
                print("Por favor ingrese un número entero positivo.")
            else:
                resultado = suma_numeros_enteros(numero)
                print(f"La suma de los números enteros desde 0 hasta {numero} es: {resultado}")
            input("Presiona Enter para continuar...")


        elif opcion == "6":
            print("Saliendo.........")
            break
        else:
            print("Opción inválida, intente de nuevo.")

if __name__ == "__main__":
    menu()
