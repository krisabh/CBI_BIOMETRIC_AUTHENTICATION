from fastapi import APIRouter, Request, Depends, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from database.db_setup import SessionLocal
from models.uidia import UIDIA
from models.medical import MedicalRecord
from models.travel import TravelRecord
from models.finance import FinanceRecord
from models.judicial import FIR, CourtHearing
import base64

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_class=HTMLResponse)
async def cbi_dashboard(request: Request):
    return templates.TemplateResponse("cbi.html", {"request": request, "aadhar_number": None, "error": None})


@router.post("/match", response_class=HTMLResponse)
async def match_thumb_image(request: Request, file: UploadFile = File(...), db: Session = Depends(get_db)):
    thumb_data = await file.read()

    user = db.query(UIDIA).filter(UIDIA.thumb_image == thumb_data).first()

    if not user:
        return templates.TemplateResponse("cbi.html", {"request": request, "aadhar_number": None,
                                                       "error": "No matching record found."})

    # Convert photo binary to base64 format
    photo_base64 = base64.b64encode(user.photo).decode("utf-8")
    photo_data_uri = f"data:image/jpeg;base64,{photo_base64}"

    # Aadhaar Card Details
    aadhar_card_details = {
        "name": user.name,
        "address": user.address,
        "aadhar_number": user.aadhar_number,
        "photo": photo_data_uri
    }

    return templates.TemplateResponse("cbi_dashboard.html", {"request": request, "aadhar_number": user.aadhar_number,
                                                             "card": aadhar_card_details})
@router.get("/fetch/{category}/{aadhar_number}", response_class=HTMLResponse)
async def fetch_records(request: Request, category: str, aadhar_number: str, db: Session = Depends(get_db)):
    data = []
    accused_alert = None

    if category == "medical":
        data = db.query(MedicalRecord).filter(MedicalRecord.aadhar_number == aadhar_number).all()
    elif category == "travel":
        data = db.query(TravelRecord).filter(TravelRecord.aadhar_number == aadhar_number).all()
    elif category == "finance":
        data = db.query(FinanceRecord).filter(FinanceRecord.aadhar_number == aadhar_number).all()
    elif category == "crime":
        fir_records = db.query(FIR).filter(FIR.aadhar_number == aadhar_number).all()
        court_records = db.query(CourtHearing).filter(CourtHearing.aadhar_number == aadhar_number).all()
        data = {"fir": fir_records, "court": court_records}

        accused_firs = db.query(FIR).filter(FIR.accused_aadhar == aadhar_number).all()
        if accused_firs:
            accused_alert = accused_firs

    return templates.TemplateResponse("cbi_details.html",
                                      {"request": request, "category": category, "records": data, "accused_alert": accused_alert})
