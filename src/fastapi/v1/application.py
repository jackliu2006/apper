from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLAEnum, create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from enum import Enum
import os

# -------------------------
# Database setup
# -------------------------
engine = create_engine(os.getenv("DATABASE_URL"), connect_args={"check_same_thread": False})
Session_Local = sessionmaker(bind=engine, autoflush=False, autocommit=False)

db_session = Session_Local()

Base = declarative_base()

class DBType(str, Enum):
    POSTGRES = "postgres"
    MYSQL = "mysql"
    SQLITE = "sqlite"

class CodeType(str, Enum):
    JAVA = "JAVA"
    PYTHON = "PYTHON"
    GO = "GO"

class ApplicationModel(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    codeStack = Column(SQLAEnum(CodeType), nullable=True)
    dbType = Column(SQLAEnum(DBType), nullable=True)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)


class Application(BaseModel):
    """An applications contains the metadata of an app which the agent is going to build up"""
    id: int
    name: str
    description: Optional[str] = None
    codeStack: Optional[CodeType] = None
    dbType: Optional[DBType] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

def create_application(app_data: Application):
    """ Create a new application in the database """
    db_app = ApplicationModel(
        name=app_data.name,
        description=app_data.description,
        codeStack=app_data.codeStack,
        dbType=app_data.dbType,
        createdAt=datetime.utcnow(),
        updatedAt=datetime.utcnow()
    )
    db_session.add(db_app)
    db_session.commit()
    db_session.refresh(db_app)
    return db_app


def get_all_applications():
    """ Retrieve all applications from the database """
    apps = db_session.query(ApplicationModel).all()
    return apps