# K-Means Clustering Flask App

Aplicación web en Flask que implementa el algoritmo K-Means Clustering para segmentar clientes de un centro comercial.

## Características

- Dataset real de 200 clientes con variables: Edad, Ingreso Anual, Puntaje de Gasto
- Algoritmo K-Means con normalización de datos
- Visualización del método del codo para selección de K
- Gráfica de clústeres con centroides
- Interfaz web responsiva con Bootstrap
- Formulario para ajustar el número de clústeres

## Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/tu-usuario/kmeans-flask-app.git
cd kmeans-flask-app
```

2. Crea un entorno virtual:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

3. Instala dependencias:
```bash
pip install -r requirements.txt
```

4. Ejecuta la aplicación:
```bash
python app.py
```

5. Abre en navegador: http://127.0.0.1:5000

## Estructura del proyecto

```
├── app.py                 # Aplicación Flask principal
├── Clustering.py          # Módulo de clustering y visualización
├── data/
│   └── mall_customers.csv # Dataset de clientes
├── templates/
│   ├── base.html          # Plantilla base
│   └── index.html         # Página principal
├── generate_dataset.py    # Script para generar dataset
└── requirements.txt       # Dependencias
```

## Tecnologías utilizadas

- Python 3.x
- Flask
- scikit-learn
- pandas
- matplotlib
- Bootstrap 4

## Dataset

El dataset contiene información sintética de 200 clientes de un centro comercial con las siguientes variables:
- CustomerID: ID único del cliente
- Gender: Género
- Age: Edad
- Annual Income (k$): Ingreso anual en miles de dólares
- Spending Score (1-100): Puntaje de gasto asignado por el centro comercial

## Algoritmo K-Means

- Normalización de datos con StandardScaler
- Selección de K usando el método del codo
- Visualización de clústeres en 2D (Ingreso vs Puntaje de Gasto)
- Cálculo de centroides

## Autor

[Tu Nombre]

## Licencia

Este proyecto es para fines educativos.
