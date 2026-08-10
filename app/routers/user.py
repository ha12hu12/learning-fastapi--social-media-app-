from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models, utils
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["User control"]
)

#Create User

@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    new_user = models.User(**user.dict())
    new_user.password = utils.hash_password(new_user.password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

#Get one user

@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 
                            f"User with id: {id} does not exist")

    return user