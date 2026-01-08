from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas.auth import RegisterSchema, TokenResponse
# قمنا بتغيير الاستيراد واستخدام Alias (UserModel) لتجنب تعارض الأسماء مع السكيما
from app.database.models import User as UserModel
from app.models.restaurant import Restaurant as RestaurantModel
from app.core.security import hash_password, verify_password, create_access_token
from app.dependencies.auth import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

# ------------------ تسجيل مستخدم عادي ------------------
@router.post("/register", status_code=201)
def register(data: RegisterSchema, db: Session = Depends(get_db)):
    # التأكد من عدم تكرار البريد الإلكتروني
    existing_user = db.query(UserModel).filter(UserModel.email == data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email already registered"
        )

    # إنشاء كائن المستخدم الجديد
    new_user = UserModel(
        name=data.name,
        email=data.email,
        password=hash_password(data.password)
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user) # لتحديث الكائن ببياناته من قاعدة البيانات (مثل الـ ID)
        return {"message": "User registered successfully"}
    except Exception as e:
        db.rollback() # تراجع عن العملية في حال حدوث خطأ أثناء الحفظ
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

# ------------------ تسجيل دخول المستخدمين العاديين ------------------
@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(UserModel).filter(UserModel.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

# ------------------ تسجيل دخول المندوبين ------------------
@router.post("/login/driver", response_model=TokenResponse)
def login_driver(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # البحث عن مستخدم بشرط أن يكون معرّف كـ سائق
    driver = db.query(UserModel).filter(
        UserModel.email == form_data.username, 
        UserModel.is_driver == True
    ).first()

    if not driver or not verify_password(form_data.password, driver.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    token = create_access_token({"sub": driver.email})
    return {"access_token": token, "token_type": "bearer"}

# ------------------ تسجيل دخول المطاعم ------------------
@router.post("/login/restaurant", response_model=TokenResponse)
def login_restaurant(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    restaurant = db.query(RestaurantModel).filter(RestaurantModel.email == form_data.username).first()

    if not restaurant or not verify_password(form_data.password, restaurant.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    token = create_access_token({"sub": restaurant.email})
    return {"access_token": token, "token_type": "bearer"}