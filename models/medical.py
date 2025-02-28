from sqlalchemy import Column, String, Integer, Date, Text
from database.db_setup import Base

class MedicalRecord(Base):
    __tablename__ = "medical_records"

    id = Column(Integer, primary_key=True, index=True)
    aadhar_number = Column(String(12), index=True)
    name = Column(String(100))
    hospital_name = Column(String(100))
    doctor_name = Column(String(100))
    diagnosis = Column(String(255))
    prescription = Column(String(255))
    visit_date = Column(Date)

    def __repr__(self):
        return f"<MedicalRecord(aadhar_number='{self.aadhar_number}', name='{self.name}')>"
