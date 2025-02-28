# models/aadhar.py

from sqlalchemy import Column, String, Integer, LargeBinary
from database.db_setup import Base

class Aadhar(Base):
    __tablename__ = "aadhar"

    id = Column(Integer, primary_key=True, index=True)
    aadhar_number = Column(String(12), unique=True, index=True)
    aadhar_card = Column(LargeBinary)  # Binary representation of the generated Aadhaar card or a path to it

    def __repr__(self):
        return f"<Aadhar(aadhar_number='{self.aadhar_number}')>"
