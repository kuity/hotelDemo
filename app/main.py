from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import models, crud
from .models import HotelResponse
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/hotels/by-hotel-ids", response_model=List[HotelResponse])
def read_hotels_by_ids(hotel_ids: str, db: Session = Depends(get_db)):
    hotel_ids_list = hotel_ids.split(',')
    hotels = crud.get_hotels_by_ids(db, hotel_ids=hotel_ids_list)
    return [HotelResponse.from_orm(hotel) for hotel in hotels]

@app.get("/hotels/by-destination-id", response_model=List[HotelResponse])
def read_hotels_by_dest_id(destination_id: int, db: Session = Depends(get_db)):
    hotels = crud.get_hotels_by_destination_id(db, destination_id=destination_id)
    return [HotelResponse.from_orm(hotel) for hotel in hotels]
