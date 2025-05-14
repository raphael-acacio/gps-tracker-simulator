from dotenv import load_dotenv
from sqlalchemy import create_engine
import os

load_dotenv()

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
db = os.getenv("DB_NAME")

engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}")

# Teste a conexão
with engine.connect() as conn:
    print("Conexão com o banco estabelecida com SQLAlchemy.")
