from .engine import engine
from .models import Session, Message
from sqlmodel import SQLModel

def create_tables():
    SQLModel.metadata.create_all(engine)

def delete_tables():
    SQLModel.metadata.drop_all(engine)
