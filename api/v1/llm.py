from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from core.database import get_db
from core.security import verify_password, create_access_token, hash_password
from repositories.user_repository import UserRepository
from models.user import User
from schemas import user
from core.ia import llmcall,agentCall

router = APIRouter(prefix="/llm", tags=["llm"])


@router.post("/llm")
def llm(prompt: str):
    resposta = agentCall(prompt)
    print(resposta)
    return {
        "response": resposta
    }