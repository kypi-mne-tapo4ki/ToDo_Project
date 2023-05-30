from pydantic import BaseModel, validator
from datetime import datetime, timezone
from beanie import PydanticObjectId


class ToDo(BaseModel):
    _id = PydanticObjectId
    title: str
    description: str
    time: datetime = None

    @validator("time", pre=True, always=True)
    def set_time_now(cls, v):
        return v or datetime.now(timezone.utc).isoformat()
