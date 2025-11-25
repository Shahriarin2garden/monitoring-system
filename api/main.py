from fastapi import FastAPI
from controllers.metrics_controller import MetricsController
from views.metrics_view import MetricsView

app = FastAPI()

@app.get("/update")
def update(users: int):
    return MetricsController.update(users)

@app.get("/cpu")
def cpu(value: float):
    return MetricsController.cpu(value)

@app.get("/metrics")
def metrics():
    registry = MetricsController.get_registry()
    return MetricsView.as_prometheus(registry)
