import asyncio

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
    tasks = []

    async with asyncio.TaskGroup() as tg:
        for city in cities:
            task = tg.create_task(fetch_temperature_data(city=city, api_url=API_URL, api_key=API_KEY, client=client))
            tasks.append((city, task))

    for city, task in tasks:
        extracted_data = task.result()
        valid_data = schemas.TemperatureCreate(city_id=city.id, **extracted_data)
        temperature = await temperature_crud.get_temperature_by_city_and_time(db=db, city_id=valid_data.city_id, date_time=valid_data.date_time)
        if temperature is None:
            temperature_crud.add_temperature(db=db, data=valid_data)
            log["created"] += 1
        else:
            log["ignored"] += 1

    await db.commit()
    return log
