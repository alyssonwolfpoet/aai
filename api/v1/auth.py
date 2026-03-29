from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from core.database import get_db
from core.security import verify_password, create_access_token, hash_password
from repositories.user_repository import UserRepository
from models.user import User
from schemas import user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
# def register(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     if UserRepository.get_by_email(db, form.username):
#         raise HTTPException(400, "Email já existe")

#     user = User(
#         email=form.username,
#         password=hash_password(form.password),
#     )
#     return UserRepository.create(db, user)@router.post("/register")

def register(user: user.UserCreate, db: Session = Depends(get_db)):
    existing = UserRepository.get_by_username(db, user.username)
    if existing:
        raise HTTPException(status_code=400, detail="Usuário já existe")

    new_user = UserRepository.create(
        db=db,
        username=user.username,
        password=hash_password(user.password),
        role="USER"
    )

    return {"message": "Usuário criado com sucesso"}

@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = UserRepository.get_by_email(db, form.username)

    if not user or not verify_password(form.password, user.password):
        raise HTTPException(400, "Credenciais inválidas")

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}