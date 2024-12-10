from fastapi import APIRouter,HTTPException,status,Response,Depends
from sqlalchemy.orm import Session
from ..import models,schema,database



router=APIRouter()


@router.post("/todos",response_model=schema.TaskResponse)
def create_todo(todo :schema.CreateTask,db :Session=Depends(database.get_db)) :
    new_todo = models.Task(**todo.dict())
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return new_todo

@router.get("/todos",response_model=list[schema.TaskResponse])
def get_todo(db :Session=Depends(database.get_db)) :
    todos = db.query(models.Task).all()
    return todos

@router.get("/todos/{todo_id}",response_model=list[schema.TaskResponse])
def get_by_id(todo_id : int,db :Session=Depends(database.get_db)) :
    one_todo = db.query(models.Task).filter(models.Task.id==todo_id).first()
    if not one_todo :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Todo Not Found")
    return [one_todo]

@router.put("/todos/update/{todo_id}",response_model=schema.TaskResponse)
def update_todo(todo_id : int , todo:schema.UpdateTask, db : Session = Depends(database.get_db)) :
    # updated_todo = db.query(models.Task).filter(models.Task.id==todo_id).update(todo.dict(),synchronize_session=False)
    updated_todo=db.query(models.Task).filter(models.Task.id==todo_id).first()
    if updated_todo is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"THE CORRESPONDING TASK WITH ID = {todo_id} NOT PRESENT IN YOUR LIST")
    for key,value in todo.dict(exclude_unset=True).items() : # Key Value pair mai loop chalake jo user key value dega usi ko update karenge baki ko ignore 
        # print(todo.dict(exclude_unset=True))
        setattr(updated_todo,key,value) # Specific Property set karta h ya update karta  h Python ka inbuilt funcn h 
    db.commit()
    db.refresh(updated_todo)
    print(updated_todo.is_complete)
    return updated_todo

@router.delete("/todos/delete/{todo_id}",status_code= status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id : int ,db : Session = Depends(database.get_db)) :
    deleted_todo = db.query(models.Task).filter(models.Task.id==todo_id).first()
    if not deleted_todo : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The corresponding Todo not found with id:{todo_id}")
    db.delete(deleted_todo)
    db.commit()
    return{"message" : "Todo Deleted Successfully"}