# TO CREATE A TOKEN AND VERIFY IT

from datetime import datetime, timedelta
import pytz
from jose import jwt
from jose.exceptions import JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from .config import Settings, settings
from . import models, schemas
from .database import get_db, Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(pytz.utc) + (
        expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        print("Decoded Token ID", id, type(id))
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=str(id))

    except JWTError:
        raise credentials_exception
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"})
    token_data = verify_access_token(token, credentials_exception)

    user = db.query(models.Users).filter(models.Users.id == token_data.id).first()
    return user
