from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict


class CityBase(BaseModel):
    name: Annotated[str, Field(max_length=100)]
    additional_info: str


class CityCreate(CityBase):
    pass


class CityRead(CityBase):
    id: int
    model_config = ConfigDict(from_attributes=True)