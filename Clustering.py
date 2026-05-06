import base64
import io

import matplotlib
matplotlib.use('Agg')  # Configurar backend no interactivo
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

DATA_PATH = "data/mall_customers.csv"
FEATURES = ["Age", "Annual Income (k$)", "Spending Score (1-100)"]


def cargar_dataset(path=DATA_PATH):
    df = pd.read_csv(path)
    df = df.dropna(subset=FEATURES)
    return df


def obtener_descripcion(df):
    return {
        "registros": int(df.shape[0]),
        "variables": FEATURES,
        "columnas": df.columns.tolist(),
        "descripcion": "Dataset de clientes para segmentación de comportamiento y gasto.",
    }


def preprocesar(df, features=FEATURES):
    X = df[features].copy()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled, scaler


def calcular_elbow(df, max_k=10):
    X_scaled, _ = preprocesar(df)
    inertias = []
    for k in range(1, max_k + 1):
        model = KMeans(n_clusters=k, random_state=42, n_init=10)
        model.fit(X_scaled)
        inertias.append(float(model.inertia_))
    return inertias


def aplicar_kmeans(df, k=4, features=FEATURES):
    X_scaled, scaler = preprocesar(df, features)
    model = KMeans(n_clusters=k, random_state=42, n_init=10)
    etiquetas = model.fit_predict(X_scaled)
    df_result = df.copy()
    df_result["Cluster"] = etiquetas.astype(int)
    return df_result, model, scaler


def fig_to_base64(fig):
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", bbox_inches="tight")
    plt.close(fig)
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode("utf-8")


def generar_grafica_clusters(df, model, scaler, x_col="Annual Income (k$)", y_col="Spending Score (1-100)"):
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "tab:brown", "tab:pink", "tab:gray"]
    for cluster in sorted(df["Cluster"].unique()):
        subset = df[df["Cluster"] == cluster]
        ax.scatter(
            subset[x_col],
            subset[y_col],
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



