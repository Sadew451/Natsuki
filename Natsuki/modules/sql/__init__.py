from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from Natsuki.conf import get_int_key, get_str_key
from Natsuki import LOGGER
DB_URI = get_str_key("SQLALCHEMY_DATABASE_URI")

def start() -> scoped_session:
    engine = create_engine(DB_URI, client_encoding="utf8")
    LOGGER.info("[PostgreSQL] Connecting to database......")
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


BASE = declarative_base()
try:
    SESSION = start()
except Exception as e:
    LOGGER.exception(f'[PostgreSQL] Failed to connect due to {e}')
    exit()
   
LOGGER.info("[PostgreSQL] Connection successful, session started.")
