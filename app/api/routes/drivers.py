from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies.auth import get_db
from app.database.models import User
from app.schemas.user import DriverCreate
from passlib.context import CryptContext

router = APIRouter(prefix="/drivers", tags=["Drivers"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register")
def register_driver(driver: DriverCreate, db: Session = Depends(get_db)):
    # تحقق من وجود المستخدم مسبقًا
    existing_user = db.query(User).filter(User.email == driver.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="المستخدم موجود مسبقًا"
        )

    # تشفير كلمة المرور
    hashed_password = pwd_context.hash(driver.password)

    # إنشاء المستخدم كمندوب
    new_driver = User(
        name=driver.name,
        email=driver.email,
        password=hashed_password,
        phone=driver.phone,
        is_driver=True
    )

    db.add(new_driver)
    db.commit()
    db.refresh(new_driver)

    return {"message": "تم تسجيل المندوب بنجاح", "driver_id": new_driver.id}
