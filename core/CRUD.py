import uuid, os, boto3,json, io
from .                 import models, schemas
from sqlalchemy.orm    import Session

BASE_DIR     = os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(__file__))))
SECRET_FILE  = os.path.join(BASE_DIR, 'secret.json')
S3           = json.loads(open(SECRET_FILE, encoding="utf8").read())['S3']

S3_FOLDER_NAME        = "qna-image"
S3_BUCKET_NAME        = S3["aws_storage_bucket_name"]
AWS_REGION_NAME       = S3["region_name"] 
AWS_ACCESS_KEY_ID     = S3["aws_access_key_id"]
AWS_SECRET_ACCESS_KEY = S3["aws_secret_access_key"]

def get_post(db : Session):
    db_post_list = db.query(models.Post).all()
    
    if not db_post_list:
        return False

    return db_post_list

async def create_post(post : schemas.PostCreate, files : list, db : Session):
    try:
        db_post = models.Post(nickname = post.nickname, password = post.password, title = post.title, content = post.content)
        db.add(db_post)
        db.commit()
        db.refresh(db_post)

        s3 = boto3.client(
            service_name = "s3", 
            region_name = AWS_REGION_NAME, 
            aws_access_key_id = AWS_ACCESS_KEY_ID,
            aws_secret_access_key = AWS_SECRET_ACCESS_KEY)

        for file in files:
            image_file = await file.read()

            file_name = f"{str(uuid.uuid4())}.jpg"

            data = io.BytesIO(image_file)

            s3.upload_fileobj(data, S3_BUCKET_NAME, f"{S3_FOLDER_NAME}/{file_name}")

            url = f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION_NAME}.amazonaws.com/{S3_FOLDER_NAME}/{file_name}"
            
            db_file = models.File(post_id = db_post.id, file_url = url)
            
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
        s3 = boto3.client(
            service_name = "s3", 
            region_name = AWS_REGION_NAME, 
            aws_access_key_id = AWS_ACCESS_KEY_ID,
            aws_secret_access_key = AWS_SECRET_ACCESS_KEY)

        db_file_urls = db.query(models.File.file_url).filter(models.File.post_id == post.id).all()
        
        for file_url in db_file_urls:
            file_name = str(file_url).split('/')[4].split('\'')[0]

            s3.delete_object(Bucket=S3_BUCKET_NAME, Key=file_name)

        db.query(models.Post).filter(models.Post.id == post.id).delete()
        db.commit()

        return True

    except Exception as e:
        db.rollback()
        db.flush()
        print(e)

        return False

async def modify_post(post : schemas.PostModify, files : list, db : Session):
    try:
        db_post = db.query(models.Post).filter(models.Post.id == post.id).first()
        
        db_post.nickname = post.nickname
        db_post.password = post.password
        db_post.title    = post.title
        db_post.content  = post.content
        
        db.add(db_post)
        db.commit()
        db.refresh(db_post)

        s3 = boto3.client(
            service_name = "s3", 
            region_name = AWS_REGION_NAME, 
            aws_access_key_id = AWS_ACCESS_KEY_ID,
            aws_secret_access_key = AWS_SECRET_ACCESS_KEY)

        db_file_urls = db.query(models.File.file_url).filter(models.File.post_id == post.id).all()
        
        for file_url in db_file_urls:
            file_name = str(file_url).split('/')[4].split('\'')[0]

            s3.delete_object(Bucket=S3_BUCKET_NAME, Key=file_name)

        for file in files:
            image_file = await file.read()

            file_name = f"{str(uuid.uuid4())}.jpg"

            data = io.BytesIO(image_file)

            s3.upload_fileobj(data, S3_BUCKET_NAME, f"{S3_BUCKET_NAME}/{file_name}")

            url = f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION_NAME}.amazonaws.com/{S3_BUCKET_NAME}/{file_name}"
            
            db_file = models.File(post_id = db_post.id, file_url = url)
            
            db.add(db_file)
            db.commit()
            db.refresh(db_file)

        return db_post, db

    except Exception as e:
        db.rollback()
        db.flush()
        print(e)

        return False, db