from turtle     import title
from pydantic   import BaseModel

class AdminLogin(BaseModel):
    email : str
    password : str

class PostCreate(BaseModel):
    nickname : str
    password : str
    title    : str
    content  : str
    

class PostPatch(BaseModel):
    id : int
    password : str

class PostModify(PostCreate):
    id : int
