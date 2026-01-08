from pydantic import BaseModel, EmailStr

# ========= Create Schemas =========

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class DriverCreate(UserCreate):
    phone: str


# ========= Response Schemas =========

class UserResponse(BaseModel):
    id: int
    name: str
    email: str


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_driver: bool
    phone: str | None
