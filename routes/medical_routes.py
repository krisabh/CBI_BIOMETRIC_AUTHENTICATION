from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
from database.db_setup import SessionLocal
from models.medical import MedicalRecord

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_class=HTMLResponse)
async def medical_form(request: Request):
    return templates.TemplateResponse("medical.html", {"request": request, "error": None})

@router.post("/submit", response_class=HTMLResponse)
async def submit_medical_record(
        request: Request,
        name: str = Form(...),
        aadhar_number: str = Form(...),
        hospital_name: str = Form(...),
        doctor_name: str = Form(...),
        diagnosis: str = Form(...),
        prescription: str = Form(...),
        visit_date: str = Form(...),
        db: Session = Depends(get_db)
):
    try:
        visit_date_obj = datetime.strptime(visit_date, "%Y-%m-%d").date()
    except ValueError:
        error_message = "Invalid date format. Please use YYYY-MM-DD."
        return templates.TemplateResponse("medical.html", {"request": request, "error": error_message})

    new_record = MedicalRecord(
        name=name,
        aadhar_number=aadhar_number,
        hospital_name=hospital_name,
        doctor_name=doctor_name,
        diagnosis=diagnosis,
        prescription=prescription,
        visit_date=visit_date_obj
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    confirmation = (
        f"<p><strong>Medical Record Submitted</strong> for <strong>{name}</strong> (Aadhaar: <strong>{aadhar_number}</strong>).</p>"
        f"<p>Details:</p>"
        f"<ul>"
        f"<li>Hospital: <strong>{hospital_name}</strong></li>"
        f"<li>Doctor: <strong>{doctor_name}</strong></li>"
        f"<li>Diagnosis: <strong>{diagnosis}</strong></li>"
        f"<li>Prescription: <strong>{prescription}</strong></li>"
        f"<li>Visit Date: <strong>{visit_date_obj.strftime('%B %d, %Y')}</strong></li>"
        f"</ul>"
    )

    return templates.TemplateResponse("medical_success.html", {
        "request": request,
        "confirmation": confirmation
    })
