from sqlalchemy import Column, String, Integer
from database.db_setup import Base

class FIR(Base):
    __tablename__ = "fir"

    id = Column(Integer, primary_key=True, index=True)
    fir_number = Column(String, unique=True, index=True)
    name = Column(String)
    aadhar_number = Column(String)
    accused_name = Column(String)
    accused_aadhar = Column(String)
    description = Column(String)

class CourtHearing(Base):
    __tablename__ = "court_hearing"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    aadhar_number = Column(String)
    case_number = Column(String, unique=True, index=True)
    court_name = Column(String)
    judge_name = Column(String)
    case_details = Column(String)
    hearing_date = Column(String)
