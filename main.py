"""
Main model as WSGI file
"""
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.router import router
from src.utils import start_up

# Save Clusters in Redis
start_up()

# Fast Api App
application = FastAPI()

origins = [
    "http://127.0.0.1",
]

application.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

application.include_router(router)
