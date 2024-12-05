from sqlalchemy import Column, Integer, String  # type: ignore
from .database import Base # type: ignore

class Resource(Base):
    __tablename__ = "resources"  # Table name in the database

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, index=True)