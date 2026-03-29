from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from core.deps import get_current_user
from core.security import hash_password

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me")
def me(user = Depends(get_current_user)):
    return user

@router.patch("/me")
def update_me(email: str | None = None,
              password: str | None = None,
              db: Session = Depends(get_db),
              user = Depends(get_current_user)):

    if email:
        user.email = email
    if password:
        user.password = hash_password(password)

    db.commit()
    return {"message": "Atualizado com sucesso"}

@router.delete("/me")
def delete_me(db: Session = Depends(get_db), user = Depends(get_current_user)):
    db.delete(user)
    db.commit()
    return {"message": "Conta deletada"}