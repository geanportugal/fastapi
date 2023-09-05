from typing import Optional
from pydantic import BaseModel as BaseSchema


class CourseSchema(BaseSchema):
    id: Optional[int]
    title: str 
    lessons: int
    hours: int 

    class Config:
        orm_mode = True
