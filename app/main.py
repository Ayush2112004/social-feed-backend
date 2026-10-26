from fastapi import Body, Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

import app.model as model
from app.database import Base, engine, get_db
from app.routes import auth, posts, user
from app.schemas import PostCreate, PostOut

Base.metadata.create_all(bind=engine)
app=FastAPI()
# class Post(BaseModel):
#     title:str
#     content:str
#     published:bool=True
#     rating:int|None=None
@app.get("/")
def home():
    return {"message":"Social Media App"}
# @app.get("/posts", response_model=list[PostOut])
# def get_posts(db: Session = Depends(get_db)):
#     posts = db.query(model.Post).all()
#     return posts

# @app.post("/posts", status_code=201, response_model=PostOut)
# def create_post(post: PostCreate, db: Session = Depends(get_db)):
#     db_post = model.Post(**post.dict())
#     db.add(db_post)
#     db.commit()
#     db.refresh(db_post)
#     return db_post
# @app.get("/posts/{id}", response_model=PostOut)
# def get_post(id:int, db: Session = Depends(get_db)):
#     post = db.query(model.Post).filter(model.Post.id==id).first()
#     if post is None:
#         raise HTTPException(status_code=404, detail="Post not found")
#     return post
# @app.delete("/posts/{id}", status_code=204)
# def delete_post(id:int, db: Session = Depends(get_db)):
#     post = db.query(model.Post).filter(model.Post.id==id).first()
#     if post is None:
#         raise HTTPException(status_code=404, detail="Post not found")
#     db.delete(post)
#     db.commit()
#     return {"message": "Post deleted successfully"}
app.include_router(user.router)
app.include_router(posts.router)
app.include_router(auth.router)
