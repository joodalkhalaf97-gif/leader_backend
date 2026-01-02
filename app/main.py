from fastapi import FastAPI
from app.database.database import engine, Base
from app.api.routes import auth, users

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Leader Backend")

app.include_router(auth.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Leader backend is running"}
