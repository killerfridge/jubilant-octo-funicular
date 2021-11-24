from ..schemas import User, UserCreate, UserValidate, UserAll
from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from typing import List
from fastapi.security import OAuth2PasswordBearer

auth_scheme = OAuth2PasswordBearer(tokenUrl='token')


router = APIRouter(
    prefix='/users',
    tags=['Users'],
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    new_user.set_password(user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/', response_model=List[UserAll])
def get_users(db: Session = Depends(get_db)):
    all_users = db.query(models.User).all()
    return all_users


@router.get('/{id}', response_model=User)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} was not found')

    return user


@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} was not found')

    db.delete(user)

    db.commit()

    return {"message": f"User {id} successfully deleted"}


@router.post('/login')
def validate_user(user: UserValidate, db: Session = Depends(get_db)):
    """Validates the user by checking the password against the hashed password in the database"""
    user_val = db.query(models.User).filter(models.User.username == user.username).first()

    if not user_val:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Username or password is incorrect")

    if user_val.check_password(user.password):
        return {"msg": "User successfully validated"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Username or password is incorrect")


def fake_hash_password(password: str):
    return "fakehashed" + password


async def fake_decode_token(token, db: Session = Depends(get_db)):
    user = await db.query(models.User).filter(models.User.username == token).first()
    return {"data": user}
    #return UserValidate(
    #    username = token + 'fakedecoded', password='testpassword'
    #)


# async def get_current_user(token: str = Depends(auth_scheme)):
#     user = await fake_decode_token(token)
#     return user


def get_current_user(token: str = Depends(auth_scheme), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == token).first()
    return user


@router.get('/me', response_model=UserValidate)
async def get_user(current_user: User = Depends(get_current_user)):
    return current_user
