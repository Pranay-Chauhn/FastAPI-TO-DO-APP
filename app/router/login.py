from fastapi import APIRouter
from fastapi import Depends, Response, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..database import Session, get_db
from .. import models, oauth2, utils
from ..schemas import Token

router = APIRouter(tags=['Authentication'])


@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    # CREATE THE TOKEN
    # RETURN THE TOKEN
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}