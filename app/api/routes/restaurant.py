from fastapi import APIRouter, Depends
from app.core.dependencies import require_restaurant  # المسار الصحيح

router = APIRouter(prefix="/restaurant", tags=["Restaurants"])

@router.get("/me")
def restaurant_me(restaurant = Depends(require_restaurant)):
    """
    استرجاع بيانات المطعم الحالي بعد تسجيل الدخول
    """
    return {
        "id": restaurant.id,
        "name": restaurant.name,
        "email": restaurant.email,
        "phone": restaurant.phone
    }
