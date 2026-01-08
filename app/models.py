from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    # أضفنا هذا السطر لمنع خطأ "Table already defined" عند إعادة تشغيل السيرفر تلقائياً
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    user_type = Column(String, nullable=False)  # لحفظ نوع الحساب
    id_number = Column(String, nullable=True)   # لحفظ رقم الهوية أو السجل
    
    # --- التعديلات الجديدة لدعم OTP ---
    is_active = Column(Boolean, default=False)  # نجعلها False افتراضياً حتى يتم التحقق
    otp_code = Column(String, nullable=True)    # حقل جديد لتخزين كود الـ 6 أرقام

    # علاقة لجلب تنبيهات المستخدم بسهولة
    notifications = relationship("Notification", back_populates="owner")


# --- جدول التنبيهات الجديد ---
class Notification(Base):
    __tablename__ = "notifications"
    # أضفنا هذا السطر هنا أيضاً لضمان استقرار الجداول المرتبطة
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    message = Column(String, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # ربط التنبيه بالمستخدم
    owner = relationship("User", back_populates="notifications")