from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import random
import string
# استيراد مكتبات إرسال الإيميل
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr

# إعدادات التشفير الموجودة مسبقاً
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "LEADER_APP_SECRET_KEY_2024" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --- إعدادات إرسال البريد الإلكتروني (SMTP) ---
# ملاحظة: يجب استخدام "App Password" من جوجل وليس كلمة مرورك العادية
conf = ConnectionConfig(
    MAIL_USERNAME = "jood.alkhalaf97@gmail.com", # بريدك هنا
    MAIL_PASSWORD = "ydaiurolsvcupxnq",    # كود الـ 16 حرفاً من جوجل هنا
    MAIL_FROM = "jood.alkhalaf97@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

# --- الدوال الخاصة بكلمة المرور والتوكن (كما هي بدون تغيير) ---

def verify_password(plain_password, hashed_password):
    return PWD_CONTEXT.verify(plain_password, hashed_password)

def get_password_hash(password):
    return PWD_CONTEXT.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- الدوال الجديدة لإرسال الـ OTP الحقيقي ---

def generate_otp():
    """توليد كود عشوائي من 6 أرقام"""
    return ''.join(random.choices(string.digits, k=6))

async def send_otp_email(email: str, otp: str):
    """إرسال إيميل حقيقي للمستخدم"""
    message = MessageSchema(
        subject="كود التحقق - تطبيق ليدر",
        recipients=[email], # قائمة المستلمين
        body=f"مرحباً بك في تطبيق ليدر، كود التحقق الخاص بك هو: {otp}",
        subtype=MessageType.plain
    )
    fm = FastMail(conf)
    await fm.send_message(message)