from fastapi import HTTPException
from models.metrics_model import MetricsModel

metrics = MetricsModel()

class MetricsController:

    @staticmethod
    def record_request(method, route, status, duration):
        """Record HTTP request metrics"""
        metrics.record_request(method, route, status, duration)

    @staticmethod
    def increment_in_progress(method, route):
        """Increment in-progress requests"""
        metrics.increment_in_progress(method, route)

    @staticmethod
    def decrement_in_progress(method, route):
        """Decrement in-progress requests"""
        metrics.decrement_in_progress(method, route)

    @staticmethod
    def record_error(error_type):
        """Record API error"""
        metrics.record_error(error_type)

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
