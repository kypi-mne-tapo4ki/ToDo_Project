from pydantic import BaseModel, validator
from datetime import datetime


class ToDo(BaseModel):
    title: str
    description: str
    time: datetime = None

    @validator("time", pre=True, always=True)
    def set_time_now(cls, v):
        return v or datetime.now()
