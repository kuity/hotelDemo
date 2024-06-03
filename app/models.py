from sqlalchemy import Column, Integer, String, Float, JSON
from .database import Base
from pydantic import BaseModel
from typing import Optional, List

class Hotel(Base):
    __tablename__ = "hotels"

    hotel_id = Column(String(20), primary_key=True, index=True)
    destination_id = Column(Integer)
    city = Column(String(30))
    postal_code = Column(String(20))
    latitude = Column(Float)
    longitude = Column(Float)
    booking_conditions = Column(JSON)
    country = Column(String(15))
    hotel_name = Column(String(50))
    address = Column(String(50))
    description = Column(String(300))
    amenities = Column(JSON)
    images = Column(JSON)

class HotelBase(BaseModel):
    destination_id: Optional[int] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    booking_conditions: Optional[List] = None
    country: Optional[str] = None
    hotel_name: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None
    amenities: Optional[dict] = None
    images: Optional[dict] = None

    class Config:
        orm_mode = True

class HotelResponse(HotelBase):
    hotel_id: str
