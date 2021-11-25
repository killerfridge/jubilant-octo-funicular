from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from ..oauth2 import get_current_user
from .. import schemas, database, models

router = APIRouter(
    prefix='/vote',
    tags=['Votes']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, user: schemas.UserAll = Depends(get_current_user), db: Session = Depends(database.get_db)):

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == user.id)
    found_vote = vote_query.first()

    if vote.direction == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User {user.username} has already liked this post: ID<{vote.post_id}>")
        new_vote = models.Vote(post_id=vote.post_id, user_id=user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vote does not exist"
            )
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully removed vote"}
