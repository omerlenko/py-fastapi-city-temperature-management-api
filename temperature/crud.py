from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import schemas
from temperature.models import Temperature


async def get_temperature_by_city_and_time(db: AsyncSession, city_id: int, date_time: datetime):
    stmt = select(Temperature).where(Temperature.city_id == city_id, Temperature.date_time == date_time)
    result = await db.scalars(stmt)
    temperature = result.one_or_none()
    return temperature

async def create_temperature(db: AsyncSession, data: schemas.TemperatureCreate) -> Temperature | None:
    temperature = await get_temperature_by_city_and_time(db=db, city_id=data.city_id, date_time=data.date_time)
    if temperature is None:
        temperature = Temperature(**data.model_dump())
        db.add(temperature)
        await db.commit()
        await db.refresh(temperature)
        return temperature
    return None
