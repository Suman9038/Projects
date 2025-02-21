from fastapi import APIRouter,HTTPException,status,Depends
from sqlalchemy.orm import Session
from ..import models,schema,database,oauth2,priority_predection
from typing import Optional



router=APIRouter()


@router.post("/todos",response_model=schema.TaskResponse)
def create_todo(todo :schema.CreateTask,db :Session=Depends(database.get_db),user_id: int= Depends(oauth2.fetch_logged_in_user)) :
    priority= priority_predection.predict_priority(todo.description) # AI se prediction kar raha h and usme function mai jo user description dera h usko pass kar dere h 
    new_todo = models.Task(user_id= user_id.id,priority=priority,**todo.dict())
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return new_todo

@router.get("/todos",response_model=list[schema.TaskResponse])
def get_todo(db :Session=Depends(database.get_db),limit:int =5,skip: int= 0,search: Optional[str]="") :
    todos = db.query(models.Task).filter(models.Task.title.contains(search)).limit(limit).offset(skip).all()
    return todos

@router.get("/user/todos",response_model=list[schema.TaskResponse])
def get_todos_for_logged_users(db: Session= Depends(database.get_db),user_id: int= Depends(oauth2.fetch_logged_in_user),limit:int =5,skip: int= 0) :
    logged_user_todos= db.query(models.Task).filter(models.Task.user_id== user_id.id).limit(limit).offset(skip).all()

    return logged_user_todos

@router.get("/todos/{todo_id}",response_model=list[schema.TaskResponse])
def get_by_id(todo_id : int,db :Session=Depends(database.get_db),user_id: int= Depends(oauth2.fetch_logged_in_user),search: Optional[str]="") :
    one_todo = db.query(models.Task).filter(models.Task.id==todo_id).filter(models.Task.title.contains(search)).first()
    if not one_todo :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Todo Not Found")
    return [one_todo]

@router.put("/todos/update/{todo_id}",response_model=schema.TaskResponse)
def update_todo(todo_id : int , todo:schema.UpdateTask, db : Session = Depends(database.get_db),user_id: int= Depends(oauth2.fetch_logged_in_user)) :
    # updated_todo = db.query(models.Task).filter(models.Task.id==todo_id).update(todo.dict(),synchronize_session=False)
    updated_todo=db.query(models.Task).filter(models.Task.id==todo_id).first()
    if updated_todo is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"THE CORRESPONDING TASK WITH ID = {todo_id} NOT PRESENT IN YOUR LIST")
    for key,value in todo.dict(exclude_unset=True).items() : # Key Value pair mai loop chalake jo user key value dega usi ko update karenge baki ko ignore 
        setattr(updated_todo,key,value) # Specific Property set karta h ya update karta  h Python ka inbuilt funcn h 

        if key == "description":
            new_priority = priority_predection.predict_priority(value)
            setattr(updated_todo, "priority", new_priority)

            
    db.commit()
    db.refresh(updated_todo)
    print(updated_todo.is_complete)
    return updated_todo

@router.delete("/todos/delete/{todo_id}",status_code= status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id : int ,db : Session = Depends(database.get_db),user_id: int= Depends(oauth2.fetch_logged_in_user),search: Optional[str]="") :
    deleted_todo = db.query(models.Task).filter(models.Task.id==todo_id).filter(models.Task.title.contains(search)).first()
    if not deleted_todo : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The corresponding Todo not found with id:{todo_id}")
    db.delete(deleted_todo)
    db.commit()
    return{"message" : "Todo Deleted Successfully"}