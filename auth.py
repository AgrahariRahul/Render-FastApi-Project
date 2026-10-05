from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime,timezone,timedelta
from fastapi import HTTPException,Depends
from dotenv import load_dotenv
import os

load_dotenv()
secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")
token_expire = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTE"))

oauth_schema = OAuth2PasswordBearer(tokenUrl="login")

def create_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=token_expire)
    to_encode.update({
        "exp":expire
    })
    return jwt.encode(to_encode,key =secret_key,algorithm=algorithm)

def verify_token(token:str = Depends(oauth_schema)):
    try:
        payload = jwt.decode(token=token,key=secret_key,algorithms=algorithm)
        return payload
    except JWTError:
        raise HTTPException(
            status_code=401,detail="invalid token"
        )
    

