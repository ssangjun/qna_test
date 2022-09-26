from .                 import models, schemas
from sqlalchemy.orm    import Session

def get_post(db : Session):
    db_post_list = db.query(models.Post).all()
    
    if not db_post_list:
        return False

    return db_post_list

def create_post(post : schemas.PostCreate, file, db : Session):
    try:
        db_post = models.Post(nickname = post.nickname, password = post.password, title = post.title, content = post.content)
        db.add(db_post)
        db.commit()
        db.refresh(db_post)

        db_file = models.File(post_id = db_post.id, file_url = file)
        db.add(db_file)
        db.commit()
        db.refresh(db_file)

        return db_post, db

    except Exception as e:
        db.rollback()
        db.flush()
        print(e)

        return False, db

def get_post_by_id(post_id : str, db : Session):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    
    if not db_post:
        return False

    return db_post

def delete_post(post : schemas.PostPatch, db : Session):
    
    try:
        db.query(models.Post).filter(models.Post.id == post.id).delete()
        db.commit()

        return True

    except Exception as e:
        db.rollback()
        db.flush()
        print(e)

        return False

def modify_post(post : schemas.PostModify, file, db : Session):
    try:
        db_post = db.query(models.Post).filter(models.Post.id == post.id).first()
        
        db_post.nickname = post.nickname
        db_post.password = post.password
        db_post.title    = post.title
        db_post.content  = post.content
        
        db.add(db_post)
        db.commit()
        db.refresh(db_post)

        db.query(models.File).filter(models.File.post_id == post.id).delete()

        db_file = models.File(post_id = post.id, file_url = file)
        
        db.add(db_file)
        db.commit()
        db.refresh(db_file)

        return db_post, db

    except Exception as e:
        db.rollback()
        db.flush()
        print(e)

        return False, db