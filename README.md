# Installation
- Create the docker container
``` ./dockerMySQL.sh ```
- Start the container
```docker start test-mysql```

# Usage
- Run the ingestion script
```python src/ingestion.py```
- Start up fastapi
```uvicorn app.main:app --reload```
- Try out the API from the browser
```
http://localhost:8000/hotels/by-hotel-ids?hotel_ids=f8c9,SjyX,iJhz
http://localhost:8000/hotels/by-destination-id?destination_id=1122
```

# Design
- Ingestion component
    - requests library used to extract the provider data
    - pandas libraty used for data cleaning and merging
    - sqlalchemy used to store the cleaned data
- Database component
    - mysql running in a docker container
- API component
    - fastapi and sqlalchemy used to serve the data via REST api
