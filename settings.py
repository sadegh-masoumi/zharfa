import os

DEBUG = os.getenv("DEBUG") == "true"

REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
