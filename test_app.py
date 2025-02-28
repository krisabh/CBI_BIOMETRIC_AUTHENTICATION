from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/ping")
async def ping():
    print("Ping endpoint reached; CWD:", os.getcwd())
    return {"message": "pong"}
