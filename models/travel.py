from sqlalchemy import Column, String, Integer, Date
from database.db_setup import Base

class TravelRecord(Base):
    __tablename__ = "travel_records"

    id = Column(Integer, primary_key=True, index=True)
    aadhar_number = Column(String(12), index=True)
    name = Column(String(100))
    mode = Column(String(20))
    transport_id = Column(String(50))  # This will be generated on the server
    transport_name = Column(String(100))  # Combined: random ID + selected transport name
    source = Column(String(100))
    destination = Column(String(100))
    date_of_journey = Column(Date)

    def __repr__(self):
        return f"<TravelRecord(id={self.id}, aadhar_number='{self.aadhar_number}', mode='{self.mode}')>"
