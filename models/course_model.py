from core.configs import settings
from sqlalchemy import Column, Integer, String


class Course(settings.DBBaseModel):
    __tablename__ = 'Course'

    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title: str = Column(String(255), name='Title')
    lessons: int = Column(Integer, name='Lessons')
    hours: int = Column(Integer, name='Hours')