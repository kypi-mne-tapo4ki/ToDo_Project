from pydantic import BaseModel, validator
from datetime import datetime, timezone


class ToDo(BaseModel):
    title: str
    description: str
    time: str = None

    @validator("time", pre=True, always=True)
    def set_time_now(cls, v):
        return v or datetime.now(timezone.utc).isoformat()
