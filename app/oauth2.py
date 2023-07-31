from jose import jwt, ExpiredSignatureError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from . import schemas, database, models
from .config import settings as set


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = set.secret_key
ALGORITHM = set.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = set.access_token_expire_time


def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encode_jwt


def verify_access_token(token: str, credentials_exepiton):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exepiton
        
        token_data = schemas.TokenData(id=id)
    
    except ExpiredSignatureError:
        raise credentials_exepiton
    
    return token_data


def get_current_user(token:str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    
    credentials_exeption = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )

    token = verify_access_token(token, credentials_exepiton=credentials_exeption)

    user = db.query(models.User).filter(models.User.id == token.id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')

    return user

