from flask import Flask, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)


@app.route("/")
def hello() -> dict:
    return {"message": "Hello from Kubernetes!", "status": "healthy"}


@app.route("/health")
def health() -> dict:
    return {"status": "ok"}


@app.route("/metrics")
def metrics_endpoint() -> str:
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
