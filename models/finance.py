from sqlalchemy import Column, String, Integer, Float
from database.db_setup import Base

class FinanceRecord(Base):
    __tablename__ = "finance_records"

    id = Column(Integer, primary_key=True, index=True)
    aadhar_number = Column(String(12), index=True)
    name = Column(String(100))
    purpose = Column(String(50))  # 'loan' or 'account'
    loan_type = Column(String(50), nullable=True)
    account_type = Column(String(50), nullable=True)
    loan_amount = Column(Float, nullable=True)  # New field for loan amount

    def __repr__(self):
        return f"<FinanceRecord(aadhar_number='{self.aadhar_number}', purpose='{self.purpose}')>"
