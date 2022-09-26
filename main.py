import uvicorn

from fastapi           import FastAPI, Depends, status, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.encoders  import jsonable_encoder

from sqlalchemy.orm    import Session

from core.user_utils   import hash_password, authenticate_post
from core.schemas      import PostCreate, PostModify, PostPatch
from core.database     import get_db
from core.CRUD         import create_post, get_post, delete_post, modify_post 

app = FastAPI()

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
async def post_upload(form_data : PostCreate, file : UploadFile = File(...), db : Session = Depends(get_db)):

    try:
        hashed_password = hash_password(form_data.password)

        form_data.password = hashed_password

        db_post, update_db = create_post(post=form_data, file=file, db=db)

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
async def post_modify(form_data : PostModify, db : Session = Depends(get_db)):

    try:
        hashed_password = hash_password(form_data.password)

        form_data.password = hashed_password

        db_post, update_db = modify_post(post=form_data, db=db)

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)