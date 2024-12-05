from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session # type: ignore
from sqlalchemy import Column, Integer, String, create_engine # type: ignore
from sqlalchemy.ext.declarative import declarative_base # type: ignore
from sqlalchemy.orm import sessionmaker # type: ignore
from pydantic import BaseModel

# SQLite database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Database engine and session
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Request model for creating a resource
class ResourceCreate(BaseModel):
    message: str

# Base class for models
Base = declarative_base()

# Model for the "resources" table
class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, index=True)

# Create all tables in the database
Base.metadata.create_all(bind=engine)

# FastAPI app instance
app = FastAPI()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route to create a resource
@app.post("/resources/")
def create_resource(resource: ResourceCreate, db: Session = Depends(get_db)):
    new_resource = Resource(message=resource.message)
    db.add(new_resource)
    db.commit()
    db.refresh(new_resource)
    return new_resource

# Route to retrieve all resources
@app.get("/resources/")
def get_resources(db: Session = Depends(get_db)):
    return db.query(Resource).all()

# Route to retrieve a single resource by ID
@app.get("/resources/{resource_id}")
def get_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource


'''
from fastapi import FastAPI, HTTPException

app = FastAPI()

# Mock data for demonstration
resources = [
    {"id": 1, "message": "Hello from Resource 1"},
    {"id": 2, "message": "This is Resource 2"},
    {"id": 3, "message": "Resource 3 says hi!"},
]

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI server!"}

@app.get("/resources")
async def get_resources():
    return resources

@app.get("/resources/{resource_id}")
async def get_resource(resource_id: int):
    resource = next((r for r in resources if r["id"] == resource_id), None)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource
'''