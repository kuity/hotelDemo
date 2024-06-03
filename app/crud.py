from sqlalchemy.orm import Session
from . import models
import json

def get_hotels_by_ids(db: Session, hotel_ids: list):
    hotels = db.query(models.Hotel).filter(models.Hotel.hotel_id.in_(hotel_ids)).all()
    for hotel in hotels:
        if isinstance(hotel.booking_conditions, str):
            hotel.booking_conditions = json.loads(hotel.booking_conditions)
        if isinstance(hotel.amenities, str):
            hotel.amenities = json.loads(hotel.amenities)
        if isinstance(hotel.images, str):
            hotel.images = json.loads(hotel.images)
    return hotels

def get_hotels_by_destination_id(db: Session, destination_id: int):
    hotels = db.query(models.Hotel).filter(models.Hotel.destination_id == destination_id).all()
    for hotel in hotels:
        if isinstance(hotel.booking_conditions, str):
            hotel.booking_conditions = json.loads(hotel.booking_conditions)
        if isinstance(hotel.amenities, str):
            hotel.amenities = json.loads(hotel.amenities)
        if isinstance(hotel.images, str):
            hotel.images = json.loads(hotel.images)
    return hotels
