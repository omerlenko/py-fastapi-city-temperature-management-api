from fastapi import APIRouter

from config import settings
from dependencies import DbDep, ClientDep
from temperature import schemas, crud as temperature_crud
from city import crud as city_crud
from temperature.client import fetch_temperature_data

API_URL = "https://api.weatherapi.com/v1/current.json"
API_KEY = settings.WEATHER_API_KEY

router = APIRouter()


@router.post("/temperatures/update/")
async def update_temperatures(db: DbDep, client: ClientDep):
    cities = await city_crud.get_cities(db=db)
    log = {
        "created": 0,
        "ignored": 0,
    }
    for city in cities:
        extracted_data = await fetch_temperature_data(city=city, api_url=API_URL, api_key=API_KEY, client=client)
        temperature_data = schemas.TemperatureCreate(city_id=city.id, **extracted_data)
        res = await temperature_crud.create_temperature(db=db, data=temperature_data)
        if res is not None:
            log["created"] += 1
        else:
            log["ignored"] += 1

    return log
