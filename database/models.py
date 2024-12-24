from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func

class Session(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now()))
    messages: List["Message"] = Relationship(back_populates="session")
    channel_id: str
    is_dm: bool
    deleted: bool = Field(default=False)

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    author: str
    text: str
    session_id: Optional[int] = Field(default=None, foreign_key="session.id")
    session: Optional[Session] = Relationship(back_populates="messages")
