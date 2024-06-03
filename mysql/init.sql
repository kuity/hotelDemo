use mysql;
CREATE TABLE IF NOT EXISTS hotels
(
    hotel_id              varchar(20),
    destination_id        int,
    city                  varchar(30),
    postal_code           varchar(20),
    latitude              double,
    longitude             double,
    booking_conditions    JSON,
    country               varchar(15),
    hotel_name            varchar(50),
    address               varchar(50),
    description           varchar(300),
    amenities             JSON,
    images                JSON
);
