from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
import time
import random
from typing import List

from .models import HealthResponse, User, UserCreate, MessageResponse

# Initialize FastAPI app
app = FastAPI(
    title="FastAPI Observability Demo",
    description="A demo service for observability with metrics, logging, and tracing",
    version="1.0.0"
)

# In-memory storage for demo purposes
users_db: List[User] = []
user_id_counter = 1


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "FastAPI Observability Demo", "timestamp": datetime.utcnow()}


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
    
    # Simulate some processing time
    await simulate_processing()
    
    # Simulate random errors (10% chance)
    if random.random() < 0.1:
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
    
    return new_user


@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    """Get a user by ID"""
    await simulate_processing()
    
    for user in users_db:
        if user.id == user_id:
            return user
    
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
    time.sleep(sleep_time)
    
    return MessageResponse(
        message=f"Slow endpoint completed after {sleep_time:.2f} seconds",
        timestamp=datetime.utcnow(),
        data={"processing_time": sleep_time}
    )


@app.get("/error")
async def error_endpoint():
    """Endpoint that always returns an error"""
    raise HTTPException(status_code=500, detail="Intentional error for testing")


async def simulate_processing():
    """Simulate random processing time"""
    # Random delay between 0.1 and 0.5 seconds
    delay = random.uniform(0.1, 0.5)
    time.sleep(delay)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
