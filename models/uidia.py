# models/uidia.py

from sqlalchemy import Column, String, Integer, LargeBinary
from database.db_setup import Base

class UIDIA(Base):
    __tablename__ = "uidia"

    id = Column(Integer, primary_key=True, index=True)
    aadhar_number = Column(String(12), unique=True, index=True)  # Unique 12-digit Aadhaar number
    name = Column(String(100))
    address = Column(String(250))
    photo = Column(LargeBinary)  # Storing photo as binary data (could also store path)
    mobile_number = Column(String(15))
    thumb_image = Column(LargeBinary)  # Storing thumb image as binary data

    def __repr__(self):
        return f"<UIDIA(aadhar_number='{self.aadhar_number}', name='{self.name}')>"
