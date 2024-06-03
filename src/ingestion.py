import requests
import json
import pandas as pd
from sqlalchemy import create_engine

amenity_list = {
    'general': [
        'pool',
        'businesscenter',
        'breakfast',
        'bar',
        'drycleaning',
        'dry cleaning',
        'business center',
        'indoor pool',
        'outdoor pool',
        'parking',
        'concierge',
        'childcare',
        'wifi'
    ]
}

def cleanAmenities(A):    
    D = {'general': [], 'room': []}
    if A is None:
        return D
    A = [x.lower().strip() for x in A]
    for a in A:
        if a in amenity_list['general']:
            D['general'].append(a)
        else:
            D['room'].append(a)
    return D

def renameDictKey(d, old_key, new_key):
    if old_key in d:
        d[new_key] = d.pop(old_key)
    return d

def cleanImages(images):
    for k in ['rooms', 'site', 'amenities']:
        replacement = []
        if k not in images.keys():
            continue
        for elem in images[k]:
            keys = elem.keys();
            if ("url" in keys):
                renameDictKey(elem, "url", "link")
            if ("caption" in keys): 
                renameDictKey(elem, "caption", "description")
    return images

def extract(url):
    response = requests.get(url)
    if response.status_code != 200:
        print("failure to ingest data")
        exit(-1)
    data = response.json()
    return pd.DataFrame(data)

def resolve_conflicts(row):
    if pd.isna(row['latitude_df1']):
        row['latitude'] = row['latitude_df2']
    elif pd.isna(row['latitude_df2']):
        row['latitude'] = row['latitude_df1']
    else:
        row['latitude'] = row['latitude_df2']

    if pd.isna(row['longitude_df1']):
        row['longitude'] = row['longitude_df2']
    elif pd.isna(row['latitude_df2']):
        row['longitude'] = row['longitude_df1']
    else:
        row['longitude'] = row['longitude_df2']

    if pd.isna(row['hotel_name_df1']):
        row['hotel_name'] = row['hotel_name_df2']
    elif pd.isna(row['hotel_name_df2']):
        row['hotel_name'] = row['hotel_name_df1']
    else:
        row['hotel_name'] = row['hotel_name_df1']

    if pd.isna(row['address_df1']):
        row['address'] = row['address_df2']
    elif pd.isna(row['address_df2']):
        row['address'] = row['address_df1']
    else:
        row['address'] = row['address_df1'] 

    if pd.isna(row['description_df1']):
        row['description'] = row['description_df2']
    elif pd.isna(row['description_df2']):
        row['description'] = row['description_df1']
    else:
        if (len(row['description_df1']) > len(row['description_df2'])):
            row['description'] = row['description_df1']
        else:
            row['description'] = row['description_df2']
            
    if pd.isna(row['amenities_df1']):
        row['amenities'] = row['amenities_df2']
    elif pd.isna(row['amenities_df2']):
        row['amenities'] = row['amenities_df1']
    else:
        row['amenities'] = {}
        row['amenities']['general'] = list(set(row['amenities_df1']['general'] + row['amenities_df2']['general']))
        row['amenities']['room'] = list(set(row['amenities_df1']['room'] + row['amenities_df2']['room']))

    return row

def resolve_conflicts2(row):
    if pd.isna(row['country_df12']):
        row['country'] = row['country_df3']
    elif pd.isna(row['country_df3']):
        row['country'] = row['country_df12']
    else:
        row['country'] = row['country_df12']

    if pd.isna(row['hotel_name_df12']):
        row['hotel_name'] = row['hotel_name_df3']
    elif pd.isna(row['hotel_name_df3']):
        row['hotel_name'] = row['hotel_name_df12']
    else:
        row['hotel_name'] = row['hotel_name_df12']

    if pd.isna(row['address_df12']):
        row['address'] = row['address_df3']
    elif pd.isna(row['address_df3']):
        row['address'] = row['address_df12']
    else:
        row['address'] = row['address_df12'] 

    if pd.isna(row['description_df12']):
        row['description'] = row['description_df3']
    elif pd.isna(row['description_df3']):
        row['description'] = row['description_df12']
    else:
        if (len(row['description_df12']) > len(row['description_df3'])):
            row['description'] = row['description_df12']
        else:
            row['description'] = row['description_df3']
            
    if pd.isna(row['amenities_df12']):
        row['amenities'] = row['amenities_df3']
    elif pd.isna(row['amenities_df3']):
        row['amenities'] = row['amenities_df12']
    else:
        row['amenities'] = {}
        row['amenities']['general'] = list(set(row['amenities_df12']['general'] + row['amenities_df3']['general']))
        row['amenities']['room'] = list(set(row['amenities_df12']['room'] + row['amenities_df3']['room']))

    if pd.isna(row['images_df12']):
        row['images'] = row['images_df3']
    elif pd.isna(row['images_df3']):
        row['images'] = row['images_df12']
    else:
        row['images'] = {}
        for k in ['site', 'amenities', 'rooms']:
            s = set()
            if k in row['images_df12']:
                for d in row['images_df12'][k]:
                    s.add(tuple(sorted(d.items())))
            if k in row['images_df3']:
                for d in row['images_df3'][k]:
                    s.add(tuple(sorted(d.items())))

            row['images'][k] = [dict(t) for t in s]
        
    return row

def saveData(df):
    username = 'root'
    password = 'password'
    host = 'localhost'
    port = '3307'
    database = 'mysql'

    # Create a connection to the database
    connection_string = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'
    engine = create_engine(connection_string)

    # Write the DataFrame to a MySQL table
    table_name = 'hotels'
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print("DataFrame saved to MySQL table successfully.")


if __name__ == "__main__":
    df = extract("https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/acme")
    df.columns = ["hotel_id", "destination_id", "hotel_name", "latitude", "longitude", "address", "city", "country", "postal_code", "description", "amenities"]
    df.latitude = pd.to_numeric(df.latitude, errors='coerce')
    df.latitude = df.latitude.astype(float)
    df.longitude = pd.to_numeric(df.latitude, errors='coerce')
    df.longitude = df.latitude.astype(float)
    df.amenities = df.amenities.apply(cleanAmenities)

    df2 = extract("https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/patagonia")
    df2.columns = ["hotel_id", "destination_id", "hotel_name", "latitude", "longitude", "address", "description", "amenities", "images"]
    df2.amenities = df2.amenities.apply(cleanAmenities)
    df2.images = df2.images.apply(cleanImages)

    df3 = extract("https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/paperflies")
    df3.columns = ["hotel_id", "destination_id", "hotel_name", "location", "description", "amenities", "images", "booking_conditions"]
    df3['address'] = df3.location.apply(lambda x: x['address'])
    df3['country'] = df3.location.apply(lambda x: x['country'])
    df3.images = df3.images.apply(cleanImages)


    df12 = pd.merge(df, df2, on=['hotel_id', 'destination_id'], how='outer', 
                    suffixes=('_df1', '_df2'))
    df12 = df12.apply(resolve_conflicts, axis=1)
    df12 = df12.drop(columns=['latitude_df1', 'latitude_df2', 'longitude_df1', 
                              'longitude_df2', 'hotel_name_df1', 'hotel_name_df2',
                              'address_df1', 'address_df2', 'description_df1', 'description_df2', 
                              'amenities_df1', 'amenities_df2'])

    df123 = pd.merge(df12, df3, on=['hotel_id', 'destination_id'], how='outer', 
                     suffixes=('_df12', '_df3'))
    df123 = df123.apply(resolve_conflicts2, axis=1)
    df123 = df123.drop(columns=['country_df12', 'country_df3', 'location', 
                                'description_df12', 'description_df3' ,'amenities_df12', 
                                'amenities_df3', 'address_df12', 'address_df3', 
                                'hotel_name_df12', 'hotel_name_df3' ,'images_df12', 'images_df3'])
    df123.booking_conditions = df123.booking_conditions.apply(json.dumps)
    df123.amenities = df123.amenities.apply(json.dumps)
    df123.images = df123.images.apply(json.dumps)
    saveData(df123)
