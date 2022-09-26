import uuid, os

from typing                  import Optional, Union, List
from pathlib                 import Path
from sqlalchemy.orm          import Session

from fastapi                 import FastAPI, Depends, status, UploadFile, File, Form
from fastapi.encoders        import jsonable_encoder
from fastapi.responses       import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from core.CRUD               import create_post, get_post, delete_post, modify_post 
from core.schemas            import PostCreate, PostModify, PostPatch
from core.database           import get_db
from core.user_utils         import hash_password, authenticate_post

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent

app.add_middleware(
  CORSMiddleware,
  allow_origins = ["*"],
  allow_methods = ["*"],
  allow_headers = ["*"],
  allow_credentials = True,
)

# @app.get("/admins/login")
# async def admin_login(form_data : AdminLogin, db : Session = Depends(get_db)):
   
@app.get("/QnA")
async def get_post_list(db : Session = Depends(get_db)):
    db_post_list = get_post(db=db)

    if not db_post_list:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="NON_PROJECT")

    return_post_list = jsonable_encoder(db_post_list)

    return JSONResponse(status_code=status.HTTP_200_OK, content=return_post_list)

@app.post("/QnA/upload")
async def post_upload( nickname = Form(), 
                       password = Form(), 
                       title    = Form(), 
                       content  = Form(), 
                       file : Union[UploadFile, None] = File(None), 
                       db : Session = Depends(get_db)):

    try:
        form_data = PostCreate
        form_data.nickname = nickname
        form_data.title    = title
        form_data.content  = content

        hashed_password = hash_password(password)

        form_data.password = hashed_password

        file_path = None

        if file:
            image_file = await file.read()

            file_name = f"{str(uuid.uuid4())}.jpg" 
            file_path = os.path.join(BASE_DIR, f"{file_name}")
            
            with open(file_path, "wb") as fp:
                fp.write(image_file)

        db_post, update_db = create_post(post=form_data, file=file_path, db=db)

        if not db_post:
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="CREATE_FAILED")
        
        return_post = jsonable_encoder(db_post)

        return JSONResponse(status_code=status.HTTP_200_OK, content=return_post)
    
    except KeyError:
        update_db.rollback()
        update_db.flush()
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="INVALID_KEYS")
    
    except ValueError:
        update_db.rollback()
        update_db.flush()
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="INVALID_INFORMATION")

    except TypeError:
        update_db.rollback()
        update_db.flush()
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="TYPE_ERROR")

@app.delete("/QnA")
async def post_delete(form_data : PostPatch, db : Session = Depends(get_db)):
    
    post = authenticate_post(post_id=form_data.id, password=form_data.password, db=db)

    if not post:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="INVALID_PASSWORD")
    
    result = delete_post(post=form_data, db=db)

    if result:
        return JSONResponse(status_code=status.HTTP_200_OK, content="SUCCESS")
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="DELETE_FAILED")

@app.post("/QnA")
async def post_authentication(form_data : PostPatch, db : Session = Depends(get_db)):
    
    post = authenticate_post(post_id=form_data.id, password=form_data.password, db=db)

    if post:
        return JSONResponse(status_code=status.HTTP_200_OK, content="SUCCESS")
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="INVALID_PASSWORD")
    
@app.patch("/QnA/upload")
async def post_modify( post_id  = Form(),
                       nickname = Form(), 
                       password = Form(), 
                       title    = Form(), 
                       content  = Form(), 
                       file : Union[UploadFile, None] = File(None), 
                       db : Session = Depends(get_db)):

    try:
        form_data = PostModify
        form_data.id       = post_id
        form_data.nickname = nickname
        form_data.title    = title
        form_data.content  = content

        hashed_password = hash_password(password)

        form_data.password = hashed_password
        
        file_path = None

        if file:
            image_file = await file.read()

            file_name = f"{str(uuid.uuid4())}.jpg" 
            file_path = os.path.join(BASE_DIR, f"{file_name}")
            
            with open(file_path, "wb") as fp:
                fp.write(image_file)

        db_post, update_db = modify_post(post=form_data, file=file_path, db=db)

        if not db_post:
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="CREATE_FAILED")
        
        return_post = jsonable_encoder(db_post)

        return JSONResponse(status_code=status.HTTP_200_OK, content=return_post)
    
    except KeyError:
        update_db.rollback()
        update_db.flush()
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="INVALID_KEYS")
    
    except ValueError:
        update_db.rollback()
        update_db.flush()
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="INVALID_INFORMATION")

    except TypeError:
        update_db.rollback()
        update_db.flush()
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="TYPE_ERROR")