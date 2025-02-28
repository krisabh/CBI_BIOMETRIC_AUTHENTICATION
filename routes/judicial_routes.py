from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import random
from database.db_setup import SessionLocal
from models.judicial import FIR, CourtHearing

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def generate_fir_number():
    return f"FIR-{random.randint(10000, 99999)}"


def generate_case_number():
    return f"CASE-{random.randint(10000, 99999)}"


@router.get("/", response_class=HTMLResponse)
async def judicial_dashboard(request: Request):
    return templates.TemplateResponse("judicial.html", {"request": request, "error": None})


@router.post("/file_fir", response_class=HTMLResponse)
async def file_fir(
        request: Request,
        name: str = Form(...),
        aadhar_number: str = Form(...),
        accused_name: str = Form(...),
        accused_aadhar: str = Form(...),
        description: str = Form(...),
        db: Session = Depends(get_db)
):
    fir_number = generate_fir_number()

    new_fir = FIR(
        fir_number=fir_number,
        name=name,
        aadhar_number=aadhar_number,
        accused_name=accused_name,
        accused_aadhar=accused_aadhar,
        description=description
    )
    db.add(new_fir)
    db.commit()
    db.refresh(new_fir)

    confirmation = (
        f"<p><strong>FIR Registered Successfully</strong> for <strong>{name}</strong> (Aadhaar: <strong>{aadhar_number}</strong>).</p>"
        f"<p>FIR Number: <strong>{fir_number}</strong></p>"
        f"<p>Accused Name: <strong>{accused_name}</strong></p>"
        f"<p>Accused Aadhaar: <strong>{accused_aadhar}</strong></p>"
        f"<p>Description: <strong>{description}</strong></p>"
    )

    return templates.TemplateResponse("judicial_success.html", {
        "request": request,
        "confirmation": confirmation
    })


@router.post("/court_hearing", response_class=HTMLResponse)
async def court_hearing(
        request: Request,
        name: str = Form(...),
        aadhar_number: str = Form(...),
        court_name: str = Form(...),
        judge_name: str = Form(...),
        case_details: str = Form(...),
        hearing_date: str = Form(...),
        db: Session = Depends(get_db)
):
    case_number = generate_case_number()

    new_hearing = CourtHearing(
        name=name,
        aadhar_number=aadhar_number,
        case_number=case_number,
        court_name=court_name,
        judge_name=judge_name,
        case_details=case_details,
        hearing_date=hearing_date
    )
    db.add(new_hearing)
    db.commit()
    db.refresh(new_hearing)

    confirmation = (
        f"<p><strong>Court Hearing Registered Successfully</strong> for <strong>{name}</strong> (Aadhaar: <strong>{aadhar_number}</strong>).</p>"
        f"<p>Case Number: <strong>{case_number}</strong></p>"
        f"<p>Court Name: <strong>{court_name}</strong></p>"
        f"<p>Judge Name: <strong>{judge_name}</strong></p>"
        f"<p>Case Details: <strong>{case_details}</strong></p>"
        f"<p>Hearing Date: <strong>{hearing_date}</strong></p>"
    )

    return templates.TemplateResponse("judicial_success.html", {
        "request": request,
        "confirmation": confirmation
    })
