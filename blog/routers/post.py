from ..database import get_db
from typing import List
from ..schemas import Post, PostCreate
from fastapi import Depends, status, HTTPException, APIRouter
from .. import models
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
async def create_posts(post: PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}")
async def get_post(id: int, db: Session = Depends(get_db)):
    post = await db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {id} not found')
    return {"data": post}


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    post = await db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {id} not found')

    await db.delete(post)
    await db.commit()

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
