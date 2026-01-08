import sys
import os
from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional

# إضافة المسار الحالي لضمان رؤية الملفات المجاورة
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# استيراد الملفات المحلية (تأكد أنها جميعاً في نفس مجلد app)
import models
import auth_utils
import database
import notifications
import websocket_manager

# --- 1. إعداد قاعدة البيانات ---
models.Base.metadata.create_all(bind=database.engine)

# --- 2. تعريف التطبيق ---
app = FastAPI(title="Leader App Backend API")
# --- 1. إعداد قاعدة البيانات ---
models.Base.metadata.create_all(bind=database.engine)

# --- 2. تعريف التطبيق ---
app = FastAPI(title="Leader App Backend API")

# --- 3. إعداد الـ CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 4. تضمين الروتر الخاص بالتنبيهات ---
app.include_router(notifications.router, tags=["Notifications"])

# --- 5. تعريف المخططات (Schemas) ---
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    user_type: str 
    id_number: Optional[str] = None

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    user_type: str
    is_active: bool
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class VerifyOTP(BaseModel):
    email: EmailStr
    otp: str

# --- 6. المسارات (Endpoints) ---
@app.get("/")
def root():
    return {"message": "Leader App Backend is Online"}

@app.post("/auth/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(database.get_db)):
    if user_in.user_type in ["مندوب", "مطعم"] and not user_in.id_number:
        raise HTTPException(status_code=400, detail=f"يرجى إدخال رقم الهوية لتعريف حسابك كـ {user_in.user_type}")
    
    existing_user = db.query(models.User).filter(models.User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="هذا البريد الإلكتروني مسجل بالفعل")
    
    otp_code = auth_utils.generate_otp()
    background_tasks.add_task(auth_utils.send_otp_email, user_in.email, otp_code)
    hashed_pass = auth_utils.get_password_hash(user_in.password)
    
    new_user = models.User(
        name=user_in.name, email=user_in.email, hashed_password=hashed_pass,
        user_type=user_in.user_type, id_number=user_in.id_number if user_in.user_type != "مستخدم عادي" else None,
        otp_code=otp_code, is_active=False 
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/auth/verify-otp")
async def verify_otp(data: VerifyOTP, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == data.email).first()
    if not user: raise HTTPException(status_code=404, detail="المستخدم غير موجود")
    if user.otp_code == data.otp:
        user.is_active = True
        user.otp_code = None
        db.commit()
        return {"message": "تم تفعيل الحساب بنجاح"}
    raise HTTPException(status_code=400, detail="كود التحقق غير صحيح")

@app.post("/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth_utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="بيانات الدخول غير صحيحة")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="يرجى تفعيل الحساب أولاً")
    access_token = auth_utils.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}