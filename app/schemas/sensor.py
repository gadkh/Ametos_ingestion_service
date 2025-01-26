from pydantic import BaseModel


class SensorResponse(BaseModel):
    device_id: str
    device_type: str

    class Config:
        orm_mode = True
