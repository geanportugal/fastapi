from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from models.course_model import Course
from schemas.course_schema import CourseSchema
from core.deps import get_session

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=CourseSchema)
async def post_course(course: CourseSchema, db: AsyncSession = Depends(get_session)):
    new_course = Course()
    new_course.title = course.title
    new_course.hours = course.hours
    new_course.lessons = course.lessons

    db.add(new_course)

    try:
        await db.commit()
        return course
    except IntegrityError:
        await db.rollback()
        raise ValueError("Title already exists.")


@router.get('/', response_model=List[CourseSchema])
async def get_courses(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Course)
        result = await session.execute(query)
        cursos: List[Course] = result.scalars().all()

        return cursos

@router.get('/{course_id}', response_model=CourseSchema, status_code=status.HTTP_200_OK)
async def get_course(course_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Course).filter(Course.id == course_id)
        result = await session.execute(query)
        course = result.scalar_one_or_none()

        if course:
            return course
        else:
            raise HTTPException(detail='Course not found.',
                                status_code=status.HTTP_404_NOT_FOUND)

# PUT curso
@router.put('/{course_id}', response_model=CourseSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_course(course_id: int, course: CourseSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Course).filter(Course.id == course_id)
        result = await session.execute(query)
        course_up = result.scalar_one_or_none()
        if course_up:
            course_up.title = course.title
            course_up.hours = course.hours
            course_up.lessons = course.lessons

            await session.commit()

            return course_up
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Course Not Fould')


@router.delete('/{course_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Course).filter(Course.id == course_id)
        result = await session.execute(query)
        course = result.scalar_one_or_none()

        if course:
            await session.delete(course)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Course not found.',
                                status_code=status.HTTP_404_NOT_FOUND)
        