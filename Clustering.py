import base64
import csv
import io

import matplotlib
matplotlib.use('Agg')  # Configurar backend no interactivo
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

DATA_PATH = "data/mall_customers.csv"
FEATURES = ["Age", "Annual Income (k$)", "Spending Score (1-100)"]


def cargar_dataset(path=DATA_PATH):
    datos = []
    with open(path, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                fila = {
                    "CustomerID": int(row["CustomerID"]),
                    "Gender": row["Gender"].strip(),
                    "Age": float(row["Age"]),
                    "Annual Income (k$)": float(row["Annual Income (k$)"]),
                    "Spending Score (1-100)": float(row["Spending Score (1-100)"]),
                }
                datos.append(fila)
            except (KeyError, ValueError):
                continue
    return datos


def obtener_descripcion(data):
    columnas = ["CustomerID", "Gender"] + FEATURES
    return {
        "registros": len(data),
        "variables": FEATURES,
        "columnas": columnas,
        "descripcion": "Dataset de clientes para segmentación de comportamiento y gasto.",
    }


def preprocesar(data, features=FEATURES):
    X = [[row[feature] for feature in features] for row in data]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled, scaler


def calcular_elbow(data, max_k=10):
    X_scaled, _ = preprocesar(data)
    inertias = []
    for k in range(1, max_k + 1):
        model = KMeans(n_clusters=k, random_state=42, n_init=10)
        model.fit(X_scaled)
        inertias.append(float(model.inertia_))
    return inertias


def aplicar_kmeans(data, k=4, features=FEATURES):
    X_scaled, scaler = preprocesar(data, features)
    model = KMeans(n_clusters=k, random_state=42, n_init=10)
    etiquetas = model.fit_predict(X_scaled)
    resultados = []
    for i, row in enumerate(data):
        fila = row.copy()
        fila["Cluster"] = int(etiquetas[i])
        resultados.append(fila)
    return resultados, model, scaler


def fig_to_base64(fig):
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", bbox_inches="tight")
    plt.close(fig)
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode("utf-8")


def generar_grafica_clusters(data, model, scaler, x_col="Annual Income (k$)", y_col="Spending Score (1-100)"):
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "tab:brown", "tab:pink", "tab:gray"]
    clusters = sorted({row["Cluster"] for row in data})
    for cluster in clusters:
        subset = [row for row in data if row["Cluster"] == cluster]
        ax.scatter(
            [row[x_col] for row in subset],
            [row[y_col] for row in subset],
            s=55,
            alpha=0.75,
            color=colors[cluster % len(colors)],
            label=f"Cluster {cluster}",
            edgecolor="white",
        )

    centroids = scaler.inverse_transform(model.cluster_centers_)
    x_idx = FEATURES.index(x_col)
    y_idx = FEATURES.index(y_col)
    ax.scatter(
        centroids[:, x_idx],
        centroids[:, y_idx],
        s=220,
        c="black",
        marker="X",
        edgecolor="white",
        linewidth=1.2,
        label="Centroides",
    )

    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_title("Clusters de clientes con centroides")
    ax.legend(loc="best", framealpha=0.85)
    ax.grid(True, linestyle="--", alpha=0.4)
    return fig_to_base64(fig)


def generar_grafica_elbow(inertias):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(range(1, len(inertias) + 1), inertias, marker="o", linestyle="-", color="#2a5d9f")
    ax.set_xlabel("Número de clústeres (K)")
    ax.set_ylabel("Inercia")
    ax.set_title("Método del codo para selección de K")
    ax.grid(True, linestyle="--", alpha=0.4)
    return fig_to_base64(fig)



