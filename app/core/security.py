from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# تبسيط التعريف لحل مشكلة KeyError
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    # نقوم بقص كلمة المرور يدوياً لضمان عدم تجاوز حد الـ 72 بايت الخاص بـ bcrypt
    # هذا يحل مشكلة الـ ValueError دون الحاجة لإعدادات إضافية
    safe_password = password[:72]
    return pwd_context.hash(safe_password)

def verify_password(plain: str, hashed: str) -> bool:
    try:
        return pwd_context.verify(plain[:72], hashed)
    except Exception:
        return False

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)