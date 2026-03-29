from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from core.deps import get_current_admin
from repositories.user_repository import UserRepository
from core.security import hash_password

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/users")
def list_users(db: Session = Depends(get_db), admin = Depends(get_current_admin)):
    return UserRepository.get_all(db)

@router.patch("/users/{user_id}")
def update_user(user_id: int,
                email: str | None = None,
                password: str | None = None,
                role: str | None = None,
                is_active: bool | None = None,
                db: Session = Depends(get_db),
                admin = Depends(get_current_admin)):

    user = UserRepository.get_by_id(db, user_id)
    if not user:
        raise HTTPException(404, "Usuário não encontrado")

    if email:
        user.email = email
    if password:
        user.password = hash_password(password)
    if role:
        user.role = role
    if is_active is not None:
        user.is_active = is_active

    db.commit()
    return {"message": "Usuário atualizado"}

@router.delete("/users/{user_id}")
def delete_user(user_id: int,
                db: Session = Depends(get_db),
                admin = Depends(get_current_admin)):

    user = UserRepository.get_by_id(db, user_id)
    if not user:
        raise HTTPException(404, "Usuário não encontrado")

    db.delete(user)
    db.commit()
    return {"message": "Usuário deletado"}