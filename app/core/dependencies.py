from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from app.database.database import get_db
from app.database.models import User
from app.models.restaurant import Restaurant  # تأكد من أن موديل المطعم موجود

SECRET_KEY = "SECRET_KEY"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# دالة للحصول على المستخدم الحالي
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="غير مصرح",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise credentials_exception

    return user


# دالة تقييد للوصول للمستخدمين العاديين
def require_user(current_user: User = Depends(get_current_user)):
    return current_user


# دالة تقييد للوصول للمندوبين فقط
def require_driver(current_user: User = Depends(get_current_user)):
    if not current_user.is_driver:
        raise HTTPException(
            status_code=403,
            detail="هذا المسار للمندوبين فقط"
        )
    return current_user


# دالة للحصول على المطعم الحالي
def get_current_restaurant(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="غير مصرح",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        restaurant_id: int | None = payload.get("sub")
        if restaurant_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise credentials_exception

    return restaurant


# دالة تقييد للوصول للمطاعم فقط
def require_restaurant(current_restaurant: Restaurant = Depends(get_current_restaurant)):
    return current_restaurant
