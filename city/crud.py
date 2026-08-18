from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city import schemas, models


async def get_cities(db: AsyncSession, skip: int = 0, limit: int = 10) -> list[models.City]:
    stmt = select(models.City).order_by(models.City.id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return list(result.scalars().all())

async def get_city(db: AsyncSession, city_id: int) -> models.City | None:
    return await db.get(models.City, city_id)

async def create_city(db: AsyncSession, data: schemas.CityCreate) -> models.City:
    city = models.City(data.model_dump())
    db.add(city)
    await db.commit()
    await db.refresh(city)
    return city
