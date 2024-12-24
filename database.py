import os
from dotenv import load_dotenv
from datetime import datetime
from typing import Optional,List
from sqlmodel import Field, SQLModel, Relationship, create_engine,Column, Session as DBSession
from sqlalchemy import Column ,DateTime, func
from sqlalchemy.sql import func
load_dotenv()

class Session(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at : datetime= Field( default_factory= datetime.utcnow)
    updated_at :datetime= Field(sa_column=Column(DateTime(timezone=True),server_default=func.now(), onupdate=func.now())) 
    messages : List["Message"]= Relationship(back_populates="session")
    channel_id : str
    is_dm: bool
    deleted : bool = Field(default=False)
    
    
    
class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at : datetime= Field(default_factory=datetime.utcnow)
    author:str
    text: str
    
    session_id: Optional[int] = Field(default=None, foreign_key="session.id")
    session: Optional[Session] = Relationship(back_populates="messages")
    
database_url=os.getenv("DATABASE_URL")
engine=create_engine(database_url , echo=True)

SQLModel.metadata.create_all(engine)
database_session = DBSession(engine)

#create
Discord_channel_1 = Session(channel_id="12345", is_dm=False)
Discord_channel_2 = Session(channel_id="54321", is_dm=True)

# add the instance
database_session.add(Discord_channel_1)
database_session.add(Discord_channel_2)

#commit the changes
database_session.commit()

def create_tables():
  SQLModel.metadata.create_all(engine)
def delete_tables():
  SQLModel.metadata.drop_all(engine)





# from sqlmodel import Field, SQLModel, Relationship, create_engine
# from typing import Optional, List
# from datetime import datetime
# from sqlalchemy.sql import func

# class SessionModel(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     created_at: datetime = Field(default_factory=datetime.utcnow)
#     updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now()))
#     messages: List["Message"] = Relationship(back_populates="session")
#     channel_id: str
#     is_dm: bool
#     deleted: bool = Field(default=False)

# class Message(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     created_at: datetime = Field(default_factory=datetime.utcnow)
#     author: str
#     text: str
#     session_id: Optional[int] = Field(default=None, foreign_key="session.id")
#     session: Optional[SessionModel] = Relationship(back_populates="messages")

# DATABASE_URL = os.getenv("DATABASE_URL")
# engine = create_engine(DATABASE_URL, echo=True)

# def create_tables():
#     SQLModel.metadata.create_all(engine)

# def delete_tables():
#     SQLModel.metadata.drop_all(engine)
