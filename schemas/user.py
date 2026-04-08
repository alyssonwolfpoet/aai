from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
    role: str | None = None
    is_active: bool | None = None
    
    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: str
    is_active: bool

    class Config:
        from_attributes = True