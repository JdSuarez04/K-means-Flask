from flask import Flask, render_template, request
import Clustering
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def inicio():
    data = Clustering.cargar_dataset()
    selected_k = int(request.form.get("k_clusters", 4)) if request.method == "POST" else 4
    resultados, modelo, scaler = Clustering.aplicar_kmeans(data, selected_k)
    grafico_clusters = Clustering.generar_grafica_clusters(resultados, modelo, scaler)
    inertias = Clustering.calcular_elbow(data)
    grafico_elbow = Clustering.generar_grafica_elbow(inertias)

    return render_template(
        "index.html",
        info=Clustering.obtener_descripcion(data),
        selected_k=selected_k,
        grafico_clusters=grafico_clusters,
        grafico_elbow=grafico_elbow,
        tabla=resultados,
        inertias=inertias,
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

