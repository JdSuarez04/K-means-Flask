from flask import Flask, render_template, request
import Clustering

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def inicio():
    df = Clustering.cargar_dataset()
    selected_k = int(request.form.get("k_clusters", 4)) if request.method == "POST" else 4
    df_clusters, modelo, scaler = Clustering.aplicar_kmeans(df, selected_k)
    grafico_clusters = Clustering.generar_grafica_clusters(df_clusters, modelo, scaler)
    inertias = Clustering.calcular_elbow(df)
    grafico_elbow = Clustering.generar_grafica_elbow(inertias)
    tabla = df_clusters.to_dict(orient="records")

    return render_template(
        "index.html",
        info=Clustering.obtener_descripcion(df),
        selected_k=selected_k,
        grafico_clusters=grafico_clusters,
        grafico_elbow=grafico_elbow,
        tabla=tabla,
        inertias=inertias,
    )

if __name__ == "__main__":
    app.run(debug=True)

