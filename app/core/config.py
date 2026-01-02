# app/core/config.py

from datetime import timedelta

# ⚠️ غيّر هذا المفتاح في الإنتاج
SECRET_KEY = "leader_backend_secret_key_change_me"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60
