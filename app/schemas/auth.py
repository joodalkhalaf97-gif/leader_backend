from pydantic import BaseModel

class RegisterSchema(BaseModel):
    name: str
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
