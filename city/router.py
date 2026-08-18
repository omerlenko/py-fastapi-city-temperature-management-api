from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from city import schemas, crud
from dependencies import get_db


router = APIRouter()
DbDep = Annotated[AsyncSession, Depends(get_db)]


@router.get("/cities/", response_model=list[schemas.CityRead])
async def read_cities(db: DbDep, skip: int = 0, limit: int = 10):
    return await crud.get_cities(db=db, skip=skip, limit=limit)