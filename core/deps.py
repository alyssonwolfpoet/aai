from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import SECRET_KEY, ALGORITHM
from repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = int(payload.get("sub"))
    user = UserRepository.get_by_id(db, user_id)
    if not user:
        raise HTTPException(401, "Usuário inválido")
    return user

def get_current_admin(user = Depends(get_current_user)):
    if user.role != "ADMIN":
        raise HTTPException(403, "Acesso apenas ADMIN")
    return user