from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models, schemas
from ..database import get_db
import bcrypt
from ..oauth2 import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid email or password")

    password_to_check = user_credentials.password[:72].encode('utf-8')
    if not bcrypt.checkpw(password_to_check, db_user.password.encode('utf-8')):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid email or password")

    access_token = create_access_token(data={"user_id": db_user.id})
    return {"access_token": access_token, "token_type": "bearer"}
