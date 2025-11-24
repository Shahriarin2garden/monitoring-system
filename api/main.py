from fastapi import FastAPI, Response
from prometheus_client import CollectorRegistry, Counter, Gauge, generate_latest

app = FastAPI()
registry = CollectorRegistry()

request_count = Counter("app_requests_total", "Total requests", registry=registry)
active_users = Gauge("app_active_users", "Active users", registry=registry)

@app.get("/update")
def update(users: int):
    request_count.inc()
    active_users.set(users)
    return {"ok": True}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(registry), media_type="text/plain")
