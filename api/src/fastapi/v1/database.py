# database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# -------------------------
# Database setup
# -------------------------
print(os.getenv("DATABASE_URL"))
Engine = create_engine(os.getenv("DATABASE_URL"), connect_args={"check_same_thread": False})
Session_Local = sessionmaker(bind=Engine, autoflush=False, autocommit=False)
DB_SESSION = Session_Local()
Base = declarative_base()