from fastapi import HTTPException
from models.metrics_model import MetricsModel

metrics = MetricsModel()

class MetricsController:

    @staticmethod
    def update(users: int):
        if users < 0:
            raise HTTPException(status_code=400, detail="Users cannot be negative")
        metrics.update_users(users)
        return {"status": "ok"}

    @staticmethod
    def cpu(value: float):
        if value < 0 or value > 100:
            raise HTTPException(status_code=400, detail="CPU must be 0–100")
        metrics.update_cpu(value)
        return {"status": "ok"}

    @staticmethod
    def get_registry():
        return metrics.registry
