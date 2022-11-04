import uuid
from typing import Optional
from pydantic import BaseModel, Field


class Test(BaseModel):
    id: int = Field(default_factory=uuid.uuid4, alias="_id")
    a: bool = Field(default=False)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {"example": {"_id": 0, "a": True}}


class TestUpdate(BaseModel):
    a: Optional[bool]

    class Config:
        schema_extra = {"example": {"a": True}}
