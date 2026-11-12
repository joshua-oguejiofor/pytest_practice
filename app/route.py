import logging
from typing import Annotated

from database import get_db
from exception import ConflictError, NotFoundError
from fastapi import APIRouter, Depends, Path
from model import TodoList
from schema import AddTodo, TodoResponse
from sqlalchemy import delete, exists, select, update
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

logger = logging.getLogger(__name__)

session_ = Annotated[AsyncSession, Depends(get_db)]

@router.get('/', response_model=list[TodoResponse], status_code=200)
async def read_todos(db: session_):
    logger.info("route accessed") 
    return (await db.execute(select(TodoList))).scalars().all()


@router.get('/{id}', response_model=TodoResponse, status_code=200)
async def get_todo_by_id(db: session_, id: int = Path(..., ge=1)):
    
    result = (await db.execute(
        select(TodoList)
        .where(TodoList.id == id)
        )).scalar_one_or_none()
    
    if not result:
        logger.info(f"todo for id: {id} not found")
        raise NotFoundError(msg="todo not found")
    
    return result


#add
@router.post('/', status_code=201)
async def add_todo(db: session_, todo: AddTodo):
    
    if await db.scalar(select(exists().where(TodoList.name == todo.name))):
        raise ConflictError(msg=f"{todo.name} already exist")
    
    new_todo = TodoList(**todo.model_dump())

    db.add(new_todo)
    await db.flush()
    await db.refresh(new_todo)
    return {"msg": f"Todo {todo.name} added successfully"}

@router.put('/{id}', status_code=200)
async def update_todo(db: session_, update_todo: AddTodo, id: int = Path(..., ge=1)):
    
    result = await db.execute(
        update(TodoList)
        .where(TodoList.id == id)
        .values(update_todo.model_dump(exclude_unset=True))
        )
    
    if result.rowcount == 0:
        logger.info(f"todo for id: {id} not found")
        raise NotFoundError(msg="Todo no found")
    
    logger.info(f"todo for id: {id} updated successfully")
    return {"msg": f"Todo for id: {id} updated successfully"}


@router.delete('/{id}', status_code= 204)
async def delete_todo(db: session_, id: int = Path(..., ge=1)):
    
    result = await db.execute(
        delete(TodoList)
        .where(TodoList.id == id)
        )
    if result.rowcount == 0:
        logger.info(f"todo for id: {id} not found")
        raise NotFoundError(msg="todo not found")
    
    logger.info(f"todo for id: {id} deleted successfully")
    
