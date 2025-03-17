from fastapi import FastAPI, Depends, HTTPException
from prometheus_client import make_asgi_app, Counter, Histogram
from sqlalchemy.orm import Session
from app import models, schemas
from app.database.session import SessionLocal, engine, Base
from app.schemas.user import User, UserCreate, UserUpdate
from app.crud.user import (
    create_user, get_users, get_user, update_user, patch_user, delete_user
)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()
@app.get("/metrics")
@app.get("/metrics/")  # Handle both with and without trailing slash
async def metrics():
    return {"message": "Metrics data here"}

# Example metrics
REQUEST_COUNT = Counter("fastapi_requests_total", "Total number of requests")
REQUEST_LATENCY = Histogram("fastapi_request_latency_seconds", "Request latency in seconds")

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.get("/")
async def root():
    REQUEST_COUNT.inc()  # Increment request count
    with REQUEST_LATENCY.time():  # Measure latency
        return {"message": "Hello, achref"}


@app.post("/users/", response_model=User)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)

@app.get("/users/", response_model=list[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update a user (full update)
@app.put("/users/{user_id}", response_model=User)
def update_user_endpoint(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = update_user(db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Patch a user (partial update)
@app.patch("/users/{user_id}", response_model=User)
def patch_user_endpoint(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = patch_user(db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Delete a user
@app.delete("/users/{user_id}", response_model=User)
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    db_user = delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user