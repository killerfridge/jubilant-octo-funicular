from ..database import get_db
from typing import List
from ..schemas import Post, PostCreate
from fastapi import Depends, status, HTTPException, APIRouter
from .. import models
from ..oauth2 import get_current_user
from sqlalchemy.orm import Session


router = APIRouter(
    prefix='/posts',
    tags=['Posts'],
)


@router.get('/', response_model=List[Post])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=Post)
async def create_posts(post: PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    new_post = models.Post(**post.dict())
    new_post.user_id = current_user.id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}")
async def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {id} not found')
    return {"data": post}


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {id} not found')

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Post with id {id} does not belong to user {current_user.id}")

    db.delete(post)
    db.commit()

    return {"message": f"Post {id} successfully deleted"}


@router.put('/{id}', status_code=status.HTTP_200_OK)
def update_post(id: int, new_post:PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {id} not found')

    post_query.update(new_post.dict(), synchronize_session=False)

    db.commit()

    return {"data": post_query.first()}
