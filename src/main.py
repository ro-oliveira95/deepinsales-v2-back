from fastapi import FastAPI

from routers import record

app = FastAPI()

app.include_router(record.router)