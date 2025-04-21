# Árbol B en Python

**Curso**: Progra-III  
**Estudiante**: Justin Rivera  
**Carnet**: 9490-23-10643

Este codigo implementa un **Árbol B configurable por grado en Python** con funciones para insertar, buscar, cargar datos desde un archivo CSV y generar una visualización del árbol mediante **Graphviz**. La opción de eliminación aún no ha sido implementada.

## 📌 Características

- Definir el grado del Árbol B al iniciar.
- Insertar un número en el árbol.
- Buscar un número en el árbol.
- Cargar datos desde un archivo CSV.
- Generar una representación gráfica del árbol B con **Graphviz**.

## 🧰 Requisitos

Asegúrate de tener instaladas las siguientes dependencias:

- **Python 3.x**
- **graphviz** (para generar gráficos visuales)

Instala las dependencias con:

```bash
pip install graphviz
```

## ▶️ Ejemplo de Uso

### ⚙️ Configuración inicial

Al iniciar el programa, se solicita el grado del Árbol B:

```
Ingrese el grado del Árbol B (mínimo 2): 3

Árbol B configurado:
- Grado del árbol: 3
- Máximo de claves por nodo: 2
- Mínimo de claves por nodo: 1
🔶 Método usado: Dividir → Agregar (grado IMPAR)
```

### 📋 Menú de opciones

```
1. Insertar número
2. Buscar número
3. Eliminar número (Por ahora, la eliminación no está implementada)
4. Cargar desde CSV
5. Visualizar con Graphviz
6. Salir
```

### ➕ Ejemplo de inserción

```
Seleccione una opción: 1
Ingrese el número a insertar: 25
Número 25 insertado en el árbol.
```

### 🔍 Ejemplo de búsqueda

```
Seleccione una opción: 2
Ingrese el número a buscar: 25
Número encontrado
```

### 🚫 Ejemplo de eliminación

```
Seleccione una opción: 3
(Por ahora, la eliminación no está implementada)
```

### 📂 Cargar desde archivo CSV

```
Seleccione una opción: 4
Ingrese la ruta del archivo CSV: datos.csv
Carga completada.
```

### 🌳 Generación del gráfico

Al seleccionar la opción **5**, se genera una imagen del árbol:

- Archivo generado: `arbol_b.png`
- Ruta: Escritorio del usuario

Se abrirá automáticamente.



