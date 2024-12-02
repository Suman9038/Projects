from fastapi import APIRouter,HTTPException,status,responses,Depends
from sqlalchemy.orm import Session
from ..import models,schema,database



router=APIRouter()


@router.post("/todos",response_model=schema.TaskRsponse)
def create_todo(todo :schema.CreateTask,db :Session=Depends(database.get_db)) :
    new_todo = models.Task(**todo.dict())
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return new_todo

@router.get("/todos",response_model=list[schema.TaskRsponse])
def get_todo(db :Session=Depends(database.get_db)) :
    todos = db.query(models.Task).all()
    return todos

@router.get("/todos/{todo_id}",response_model=list[schema.TaskRsponse])
def get_by_id(todo_id : int,db :Session=Depends(database.get_db)) :
    todo = db.query(models.Task).filter(models.Task.id==todo_id).first()
    if not todo :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Todo Not Found")
    return [todo]