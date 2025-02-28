# main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Import routers
from routes import (
    medical_routes,
    travel_routes,
    finance_routes,
    judicial_routes,
    aadhar_routes,
    cbi_routes
)

app = FastAPI()

# Mount static directory (for CSS, JS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="templates")

# Include routers with prefixes and tags
app.include_router(medical_routes.router, prefix="/medical", tags=["Medical"])
app.include_router(travel_routes.router, prefix="/travel", tags=["Travel"])
app.include_router(finance_routes.router, prefix="/finance", tags=["Finance"])
app.include_router(judicial_routes.router, prefix="/crime", tags=["Crime"])
app.include_router(aadhar_routes.router, prefix="/aadhar", tags=["Aadhaar"])
app.include_router(cbi_routes.router, prefix="/cbi", tags=["Unified"])

@app.get("/")
async def home():
    return {"message": "Welcome to the Biometric System!"}
@app.get("/ping")
async def ping():
    return {"message": "pong"}



