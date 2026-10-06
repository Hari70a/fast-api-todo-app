from fastapi import FastAPI
from .models import Base
from .database import engine
from .routers import auth, admin, todos, users

app = FastAPI()

# models.Base.metadata.create_all(bind=engine)
Base.metadata.create_all(bind=engine)

@app.get("/healthy")
def health_check():
    return { "status": "healthy" }

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)



