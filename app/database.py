from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# اسم قاعدة البيانات
SQLALCHEMY_DATABASE_URL = "sqlite:///./leader.db"

# إنشاء المحرك (Engine) - تم حذف create_client الخطأ
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# إنشاء الجلسة
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# الكلاس الأساسي للموديلات
Base = declarative_base()

# دالة الحصول على قاعدة البيانات
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()