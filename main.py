from fastapi import FastAPI
from pymongo import MongoClient
from routes import *


app = FastAPI()
# app.mongodb_client = MongoClient("localhost", 27017)
# app.database = app.mongodb_client["fastt"]
@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(
        "mongodb+srv://onwords:onwords8182@cluster0.ibaw2uh.mongodb.net/?retryWrites=true&w=majority&ssl=true"
    )
    app.database = app.mongodb_client["db1"]


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(testrouter, tags=["Test"], prefix="")
