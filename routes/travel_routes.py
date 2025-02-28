from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
import random
from database.db_setup import SessionLocal
from models.travel import TravelRecord

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def generate_transport_id():
    # Generate a random 5-digit transport ID as a string.
    return f"{random.randint(10000, 99999)}"


@router.get("/", response_class=HTMLResponse)
async def travel_form(request: Request):
    # Define transport options for each mode.
    flight_options = ["INDIGO", "SPICEJET", "AIR INDIA", "AIR ASIA"]
    train_options = ["VANDE BHARAT", "JAN SHATABDI", "GAREEN RATH", "DODRONTO EXPRESS"]
    bus_options = ["VRL Travels", "SRS Travels", "Odbus", "RedBus"]
    return templates.TemplateResponse("travel.html", {
        "request": request,
        "error": None,
        "flight_options": flight_options,
        "train_options": train_options,
        "bus_options": bus_options
    })


@router.post("/book", response_class=HTMLResponse)
async def book_travel(
        request: Request,
        name: str = Form(...),
        aadhar_number: str = Form(...),
        mode: str = Form(...),
        transport_name: str = Form(...),
        source: str = Form(...),
        destination: str = Form(...),
        date_of_journey: str = Form(...),
        db: Session = Depends(get_db)
):
    # Validate and convert the journey date.
    try:
        journey_date = datetime.strptime(date_of_journey, "%Y-%m-%d").date()
    except ValueError:
        error_message = "Invalid date format. Please use YYYY-MM-DD."
        return templates.TemplateResponse("travel.html", {"request": request, "error": error_message})

    # Generate the transport id on the server side.
    random_transport_id = generate_transport_id()
    full_transport_name = f"{random_transport_id}-{transport_name}"

    # Create a new travel record.
    new_record = TravelRecord(
        name=name,
        aadhar_number=aadhar_number,
        mode=mode,
        transport_id=random_transport_id,
        transport_name=full_transport_name,
        source=source,
        destination=destination,
        date_of_journey=journey_date
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    # Build a human-readable confirmation message.
    confirmation = (
        f"<p><strong>{mode.title()}</strong> has been booked successfully for <strong>{name}</strong> "
        f"with Aadhaar number <strong>{aadhar_number}</strong>.</p>"
        f"<p>Details:</p>"
        f"<ul>"
        f"<li>Transport: <strong>{full_transport_name}</strong></li>"
        f"<li>From: <strong>{source}</strong> To: <strong>{destination}</strong></li>"
        f"<li>Date: <strong>{journey_date.strftime('%B %d, %Y')}</strong></li>"
        f"</ul>"
    )

    return templates.TemplateResponse("travel_success.html", {"request": request, "confirmation": confirmation})
