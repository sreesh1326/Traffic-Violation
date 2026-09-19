from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from auth.router import router as auth_router

Base.metadata.create_all(bind = engine)

app = FastAPI(title = "traffic violation detection API")
app.add_middleware(CORSMiddleware, allow_origins = ["http://localhost:3000"],
                   allow_credentials = True,
                   allow_methods = ["*"],
                   allow_headers = ["*"]
                   )
                   
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Welcome to the traffic violation detection API!"}
                   
