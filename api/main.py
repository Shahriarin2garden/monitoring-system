from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from controllers.metrics_controller import MetricsController
from views.metrics_view import MetricsView
import time
import asyncio
import random

app = FastAPI(title="API Monitoring System")

# Middleware for request metrics
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    """Middleware to track request metrics"""
    method = request.method
    path = request.url.path
    
    # Skip metrics endpoint to avoid recursion
    if path == "/metrics":
        return await call_next(request)
    
    # Increment in-progress counter
    MetricsController.increment_in_progress(method, path)
    
    start_time = time.time()
    try:
        response = await call_next(request)
        duration = time.time() - start_time
        status = response.status_code
        
        # Record metrics
        MetricsController.record_request(method, path, status, duration)
        
        return response
    except Exception as e:
        duration = time.time() - start_time
        MetricsController.record_error(type(e).__name__)
        MetricsController.record_request(method, path, 500, duration)
        raise
    finally:
        # Decrement in-progress counter
        MetricsController.decrement_in_progress(method, path)

# Health check endpoint
@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "api-monitoring"}

# Metrics endpoint
@app.get("/metrics")
def metrics():
    """Prometheus metrics endpoint"""
    registry = MetricsController.get_registry()
    return MetricsView.as_prometheus(registry)

# User management endpoints
users_db = {}
next_user_id = 1

@app.get("/api/users")
def list_users():
    """List all users"""
    return {"users": list(users_db.values()), "count": len(users_db)}

@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    """Get user by ID"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]

@app.post("/api/users")
def create_user(name: str, email: str):
    """Create a new user"""
    global next_user_id
    user_id = next_user_id
    next_user_id += 1
    user = {"id": user_id, "name": name, "email": email}
    users_db[user_id] = user
    return user

@app.put("/api/users/{user_id}")
def update_user(user_id: int, name: str = None, email: str = None):
    """Update user"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    if name:
        users_db[user_id]["name"] = name
    if email:
        users_db[user_id]["email"] = email
    return users_db[user_id]

@app.delete("/api/users/{user_id}")
def delete_user(user_id: int):
    """Delete user"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    user = users_db.pop(user_id)
    return {"message": "User deleted", "user": user}

# Slow endpoint for latency testing
@app.get("/api/slow")
async def slow_endpoint():
    """Simulated slow endpoint (2-3 second delay)"""
    delay = random.uniform(2, 3)
    await asyncio.sleep(delay)
    return {"message": "Slow endpoint response", "delay_seconds": delay}

# Error endpoint for error tracking
@app.get("/api/error")
def error_endpoint():
    """Simulated error endpoint"""
    raise HTTPException(status_code=500, detail="Simulated API error")

# Legacy endpoints for backward compatibility
@app.get("/update")
def update(users: int):
    return MetricsController.update(users)

@app.get("/cpu")
def cpu(value: float):
    return MetricsController.cpu(value)
