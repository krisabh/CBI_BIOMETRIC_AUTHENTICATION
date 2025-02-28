from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database.db_setup import SessionLocal
from models.finance import FinanceRecord

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/test", response_class=HTMLResponse)
async def test_finance(request: Request):
    return templates.TemplateResponse("finance_success.html", {"request": request, "confirmation": "<p>Test message</p>"})

@router.get("/", response_class=HTMLResponse)
async def finance_form(request: Request):
    return templates.TemplateResponse("finance.html", {"request": request, "error": None})


@router.post("/record", response_class=HTMLResponse)
async def add_finance_record(
        request: Request,
        aadhar_number: str = Form(...),
        name: str = Form(...),
        purpose: str = Form(...),
        loan_type: str = Form(None),
        account_type: str = Form(None),
        loan_amount: float = Form(None),
        db: Session = Depends(get_db)
):
    new_record = FinanceRecord(
        aadhar_number=aadhar_number,
        name=name,
        purpose=purpose,
        loan_type=loan_type,
        account_type=account_type,
        loan_amount=loan_amount
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    if purpose.lower() == "loan":
        confirmation = (
            f"<p>A loan application has been submitted for <strong>{name}</strong> (Aadhaar: <strong>{aadhar_number}</strong>).</p>"
            f"<p>Loan Type: <strong>{loan_type}</strong></p>"
            f"<p>Loan Amount: <strong>{loan_amount}</strong></p>"
        )
    elif purpose.lower() == "account":
        confirmation = (
            f"<p>An account has been opened for <strong>{name}</strong> (Aadhaar: <strong>{aadhar_number}</strong>).</p>"
            f"<p>Account Type: <strong>{account_type}</strong></p>"
        )
    else:
        confirmation = f"<p>Finance record submitted for <strong>{name}</strong>.</p>"

    print("Returning success template with confirmation:", confirmation)
    return templates.TemplateResponse("finance_success.html", {"request": request, "confirmation": confirmation})
