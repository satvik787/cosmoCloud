from fastapi import FastAPI
import uvicorn
from pymongo import MongoClient
from controller.student import router,Request,Response,status
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
import os
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.environ.get("DB_URL")
DB_NAME = os.environ.get("DB_NAME")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.middleware("http")
async def handleAllException(req:Request,call_next):
    try:
        return await call_next(req)
    except Exception as e:
        print(e)
        return Response("Internal Server Error",status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


app.client = MongoClient(DB_URL)
app.db = app.client[DB_NAME]

app.include_router(router, prefix="/students")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)