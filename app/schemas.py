from pydantic import BaseModel, EmailStr
from typing import Optional

# هذا المخطط لاستقبال بيانات التسجيل من Flutter
class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    user_type: str  # مستخدم عادي، مندوب، مطعم
    id_number: Optional[str] = None

# هذا المخطط لإرجاع بيانات المستخدم بعد النجاح (UserOut)
class UserOut(BaseModel):
    id: int
    name: str
    email: str
    user_type: str

    class Config:
        from_attributes = True

# هذا المخطط لإرجاع التوكن عند تسجيل الدخول
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None