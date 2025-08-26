from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from datetime import datetime
import time
import random
from typing import List
from prometheus_fastapi_instrumentator import Instrumentator
import logging

from .models import HealthResponse, User, UserCreate, MessageResponse
from .logging_config import setup_logging

# Setup logging
logger = setup_logging()

# Initialize FastAPI app
app = FastAPI(
    title="FastAPI Observability Demo",
    description="A demo service for observability with metrics, logging, and tracing",
    version="1.0.0"
)

# Initialize Prometheus metrics
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

# Custom metrics
from prometheus_client import Counter, Histogram, Gauge
import asyncio

# Custom Prometheus metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency', ['method', 'endpoint'])
ACTIVE_USERS = Gauge('active_users_total', 'Total number of active users')
ERROR_COUNT = Counter('http_errors_total', 'Total HTTP errors', ['method', 'endpoint', 'error_type'])

# Middleware for custom metrics and logging
@app.middleware("http")
async def metrics_and_logging_middleware(request: Request, call_next):
    start_time = time.time()
    
    # Log incoming request
    logger.info(
        "Incoming request",
        extra={
            "method": request.method,
            "url": str(request.url),
            "path": request.url.path,
            "query_params": str(request.query_params),
            "client_ip": request.client.host if request.client else None,
            "user_agent": request.headers.get("user-agent"),
            "request_id": id(request)
        }
    )
    
    # Process the request
    response = await call_next(request)
    
    # Calculate metrics
    process_time = time.time() - start_time
    endpoint = request.url.path
    method = request.method
    status_code = str(response.status_code)
    
    # Update metrics
    REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status_code).inc()
    REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(process_time)
    
    # Update active users count (based on current users in memory)
    ACTIVE_USERS.set(len(users_db))
    
    # Track errors
    if response.status_code >= 400:
        error_type = "client_error" if response.status_code < 500 else "server_error"
        ERROR_COUNT.labels(method=method, endpoint=endpoint, error_type=error_type).inc()
    
    # Log response
    log_level = logging.ERROR if response.status_code >= 500 else logging.WARNING if response.status_code >= 400 else logging.INFO
    logger.log(
        log_level,
        "Request completed",
        extra={
            "method": method,
            "endpoint": endpoint,
            "status_code": response.status_code,
            "process_time": process_time,
            "request_id": id(request)
        }
    )
    
    return response

# In-memory storage for demo purposes
users_db: List[User] = []
user_id_counter = 1


@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    logger.info(
        "FastAPI application starting up",
        extra={
            "app_name": "FastAPI Observability Demo",
            "version": "1.0.0",
            "startup_time": datetime.utcnow().isoformat()
        }
    )


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    logger.info(
        "FastAPI application shutting down",
        extra={
            "app_name": "FastAPI Observability Demo",
            "shutdown_time": datetime.utcnow().isoformat(),
            "total_users_created": len(users_db)
        }
    )


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "FastAPI Observability Demo", "timestamp": datetime.utcnow()}


@app.get("/metrics-info")
async def metrics_info():
    """Information about available metrics"""
    return {
        "message": "Prometheus metrics are available at /metrics endpoint",
        "custom_metrics": [
            "http_requests_total - Total HTTP requests",
            "http_request_duration_seconds - HTTP request latency", 
            "active_users_total - Total number of active users",
            "http_errors_total - Total HTTP errors"
        ],
        "standard_metrics": "Available via prometheus-fastapi-instrumentator",
        "timestamp": datetime.utcnow()
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow()
    )


@app.get("/users", response_model=List[User])
async def get_users():
    """Get all users"""
    # Simulate some processing time
    await simulate_processing()
    return users_db


@app.post("/users", response_model=User)
async def create_user(user: UserCreate):
    """Create a new user"""
    global user_id_counter
    
    logger.info(
        "Creating new user",
        extra={
            "user_name": user.name,
            "user_email": user.email,
            "user_age": user.age,
            "current_user_count": len(users_db)
        }
    )
    
    # Simulate some processing time
    await simulate_processing()
    
    # Simulate random errors (10% chance)
    if random.random() < 0.1:
        logger.error(
            "Random server error occurred during user creation",
            extra={
                "user_name": user.name,
                "user_email": user.email,
                "error_type": "random_error"
            }
        )
        raise HTTPException(status_code=500, detail="Random server error")
    
    new_user = User(
        id=user_id_counter,
        name=user.name,
        email=user.email,
        age=user.age,
        created_at=datetime.utcnow()
    )
    
    users_db.append(new_user)
    user_id_counter += 1
    
    logger.info(
        "User created successfully",
        extra={
            "user_id": new_user.id,
            "user_name": new_user.name,
            "user_email": new_user.email,
            "total_users": len(users_db)
        }
    )
    
    return new_user


@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    """Get a user by ID"""
    logger.info(
        "Retrieving user by ID",
        extra={
            "user_id": user_id,
            "total_users": len(users_db)
        }
    )
    
    await simulate_processing()
    
    for user in users_db:
        if user.id == user_id:
            logger.info(
                "User found",
                extra={
                    "user_id": user_id,
                    "user_name": user.name,
                    "user_email": user.email
                }
            )
            return user
    
    logger.warning(
        "User not found",
        extra={
            "user_id": user_id,
            "total_users": len(users_db)
        }
    )
    raise HTTPException(status_code=404, detail="User not found")


@app.delete("/users/{user_id}", response_model=MessageResponse)
async def delete_user(user_id: int):
    """Delete a user by ID"""
    await simulate_processing()
    
    for i, user in enumerate(users_db):
        if user.id == user_id:
            deleted_user = users_db.pop(i)
            return MessageResponse(
                message=f"User {deleted_user.name} deleted successfully",
                timestamp=datetime.utcnow(),
                data={"deleted_user_id": user_id}
            )
    
    raise HTTPException(status_code=404, detail="User not found")


@app.get("/slow")
async def slow_endpoint():
    """Endpoint that simulates slow processing"""
    # Simulate slow processing (2-5 seconds)
    sleep_time = random.uniform(2, 5)
    
    logger.info(
        "Starting slow processing",
        extra={
            "expected_sleep_time": sleep_time,
            "endpoint": "/slow"
        }
    )
    
    time.sleep(sleep_time)
    
    logger.info(
        "Slow processing completed",
        extra={
            "actual_sleep_time": sleep_time,
            "endpoint": "/slow"
        }
    )
    
    return MessageResponse(
        message=f"Slow endpoint completed after {sleep_time:.2f} seconds",
        timestamp=datetime.utcnow(),
        data={"processing_time": sleep_time}
    )


@app.get("/error")
async def error_endpoint():
    """Endpoint that always returns an error"""
    logger.error(
        "Intentional error endpoint called",
        extra={
            "endpoint": "/error",
            "error_type": "intentional"
        }
    )
    raise HTTPException(status_code=500, detail="Intentional error for testing")


async def simulate_processing():
    """Simulate random processing time"""
    # Random delay between 0.1 and 0.5 seconds
    delay = random.uniform(0.1, 0.5)
    time.sleep(delay)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
