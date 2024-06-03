import unittest
from unittest.mock import MagicMock
from app.crud import get_hotels_by_ids
from app.models import Hotel

class TestCrud(unittest.TestCase):
    def setUp(self):
        # Create a mock session
        self.db = MagicMock()

        # Example data
        self.example_hotels = [
            Hotel(
                hotel_id="1",
                destination_id=100,
                city="CityA",
                postal_code="12345",
                latitude=10.0,
                longitude=20.0,
                booking_conditions=[],
                country="CountryA",
                hotel_name="HotelA",
                address="AddressA",
                description="DescriptionA",
                amenities={},
                images={}
            ),
            Hotel(
                hotel_id="2",
                destination_id=200,
                city="CityB",
                postal_code="67890",
                latitude=15.0,
                longitude=25.0,
                booking_conditions=[],
                country="CountryB",
                hotel_name="HotelB",
                address="AddressB",
                description="DescriptionB",
                amenities={},
                images={}
            )
        ]

    def test_get_hotels_by_ids(self):
        # Mock the query result
        self.db.query().filter().all.return_value = self.example_hotels

        # Call the function with mock data
        hotel_ids = ["1", "2"]
        result = get_hotels_by_ids(self.db, hotel_ids)

        # Check the result
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].hotel_id, "1")
        self.assertEqual(result[1].hotel_id, "2")

        # Verify the query calls
        self.db.query().filter().all.assert_called_once()

if __name__ == "__main__":
    unittest.main()
