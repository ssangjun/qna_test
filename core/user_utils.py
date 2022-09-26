import bcrypt
from . import CRUD
from sqlalchemy.orm    import Session

def hash_password(password : str):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    return hashed_password

def authenticate_post(post_id : str, password : str, db : Session):
    db_post = CRUD.get_post_by_id(post_id=post_id, db=db)

    if not db_post:
        return False

    checked_password = bcrypt.checkpw(password.encode('utf-8'), db_post.password.encode('utf-8'))

    if not checked_password:
        return False
    
    return db_post