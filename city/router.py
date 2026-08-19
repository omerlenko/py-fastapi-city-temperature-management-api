from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from city import schemas, crud
from dependencies import get_db


router = APIRouter()
DbDep = Annotated[AsyncSession, Depends(get_db)]


@router.get("/cities/", response_model=list[schemas.CityRead])
async def read_cities(db: DbDep, skip: int = 0, limit: int = 10):
    return await crud.get_cities(db=db, skip=skip, limit=limit)

@router.get("/cities/{city_id}/", response_model=schemas.CityRead)
async def read_city(db: DbDep, city_id: int):
    city = await crud.get_city(db=db, city_id=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="This city does not exist in the database")
    return city

@router.post("/cities/", response_model=schemas.CityRead, status_code=201)
async def create_city(db: DbDep, data: schemas.CityCreate):
    try:
        city = await crud.create_city(db=db, data=data)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="A city with this name already exists")
    return city

@router.patch("/cities/{city_id}/", response_model=schemas.CityRead)
async def update_city(db: DbDep, city_id: int, data: schemas.CityUpdate):
    city = await crud.get_city(db=db, city_id=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="This city does not exist in the database")
    try:
        return await crud.update_city(db=db, city=city, data=data)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="A city with this name already exists")

@router.delete("/cities/{city_id}/", status_code=204)
async def delete_city(db: DbDep, city_id: int):
    city = await crud.get_city(db=db, city_id=city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="This city does not exist in the database")
    await crud.delete_city(db=db, city=city)
