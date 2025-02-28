from fastapi import APIRouter, Request, Form, UploadFile, File, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database.db_setup import SessionLocal
from models.uidia import UIDIA
from models.aadhar import Aadhar
import random
import base64

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def generate_aadhar_number():
    return "".join([str(random.randint(0, 9)) for _ in range(12)])


@router.get("/", response_class=HTMLResponse)
async def aadhaar_form(request: Request):
    return templates.TemplateResponse("aadhar.html", {"request": request, "error": None})


@router.post("/register", response_class=HTMLResponse)
async def register_aadhaar(
        request: Request,
        name: str = Form(...),
        address: str = Form(...),
        mobile_number: str = Form(...),
        thumb_image: UploadFile = File(...),
        photo: UploadFile = File(None),
        photo_data: str = Form(None),
        db: Session = Depends(get_db)
):
    # Read thumb image (mandatory)
    thumb_bytes = await thumb_image.read()

    # Check if thumb image is already registered.
    existing = db.query(UIDIA).filter(UIDIA.thumb_image == thumb_bytes).first()
    if existing:
        error_message = f"You are already registered with Aadhaar number {existing.aadhar_number}."
        return templates.TemplateResponse("aadhar.html", {"request": request, "error": error_message})

    # Check that a photo is provided (either via file or camera capture).
    if not photo_data and not photo:
        error_message = "Photo is mandatory. Please either upload a photo or capture one using the camera."
        return templates.TemplateResponse("aadhar.html", {"request": request, "error": error_message})

    # Process photo: prioritize photo_data from camera if provided.
    if photo_data:
        try:
            # Expect photo_data in the format "data:image/jpeg;base64,..."
            header, encoded = photo_data.split(",", 1)
            photo_bytes = base64.b64decode(encoded)
        except Exception as e:
            error_message = "Invalid photo data provided."
            return templates.TemplateResponse("aadhar.html", {"request": request, "error": error_message})
    else:
        # Read the uploaded photo file.
        photo_bytes = await photo.read()
        if not photo_bytes:
            error_message = "Uploaded photo is empty. Please provide a valid photo."
            return templates.TemplateResponse("aadhar.html", {"request": request, "error": error_message})

    # At this point, we have a valid photo and thumb_bytes.
    # Generate a new Aadhaar number.
    aadhar_number = generate_aadhar_number()

    new_user = UIDIA(
        aadhar_number=aadhar_number,
        name=name,
        address=address,
        photo=photo_bytes,
        mobile_number=mobile_number,
        thumb_image=thumb_bytes
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Optionally store in Aadhar table.
    aadhar_card_data = b"Sample Aadhaar Card Data for " + aadhar_number.encode()
    new_aadhar = Aadhar(
        aadhar_number=aadhar_number,
        aadhar_card=aadhar_card_data
    )
    db.add(new_aadhar)
    db.commit()
    db.refresh(new_aadhar)

    # Convert photo to a base64 data URI for embedding.
    photo_base64 = base64.b64encode(photo_bytes).decode("utf-8")
    photo_data_uri = f"data:image/jpeg;base64,{photo_base64}"

    aadhar_card_details = {
        "name": name,
        "address": address,
        "aadhar_number": aadhar_number,
        "photo": photo_data_uri
    }

    return templates.TemplateResponse("aadhar_card.html", {"request": request, "card": aadhar_card_details})
