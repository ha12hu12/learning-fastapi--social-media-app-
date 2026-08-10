from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db 
from .. import schemas, models, oauth2, utils

router = APIRouter(
    prefix="/login",
    tags=["Login Control"]
)

@router.post("/", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):

    #The OAuth2PasswordRequestForm doesn't have (email) row, it has (username) row
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status.HTTP_403_FORBIDDEN, f"Invalid credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status.HTTP_403_FORBIDDEN, f"Invalid credentials")

    return {"access_token": oauth2.create_access_token({"user_id": user.id}),
            "token_type": "bearer"}

 


