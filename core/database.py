import os,json 
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm             import sessionmaker

BASE_DIR     = os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(__file__))))
SECRET_FILE  = os.path.join(BASE_DIR, 'secret.json')
DB           = json.loads(open(SECRET_FILE, encoding="utf8").read())['DB']
DATABASE_URL = f"mysql+pymysql://{DB['user']}:{DB['password']}@{DB['host']}:{DB['port']}/{DB['database']}?charset=utf8mb4"

engine = create_engine(DATABASE_URL)

# 얘네 역할이 뭔지1
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# 얘네 역할이 뭔지2
Base = declarative_base()

def get_db():
    db = SessionLocal()

    try:
        yield db
    
    finally:
        db.close()

print()