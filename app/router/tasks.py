from fastapi import APIRouter, Depends, Response, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import models, schemas, oauth2

router = APIRouter(
    prefix="/tasks",  # Added a prefix to avoid redundant `/task/` in routes
    tags=['Tasks']
)


# Get all tasks for the logged-in user
@router.get("/", response_model=List[schemas.Task])
async def get_tasks(db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user)):
    tasks = db.query(models.Tasks).filter(models.Tasks.owner_id == current_user.id).all()
    return tasks


# Create a new task
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Task)
async def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db),
                      current_user: int = Depends(oauth2.get_current_user)):
    new_task = models.Tasks(owner_id=current_user.id, **task.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


# Get a single task by ID
@router.get("/{id}", response_model=schemas.Task)
async def get_task(id: int, db: Session = Depends(get_db),
                   current_user: int = Depends(oauth2.get_current_user)):
    task = db.query(models.Tasks).filter(models.Tasks.id == id, models.Tasks.owner_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Task with id {id} not found")
    return task


# Delete a task
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(id: int, db: Session = Depends(get_db),
                      current_user: int = Depends(oauth2.get_current_user)):
    task = db.query(models.Tasks).filter(models.Tasks.id == id, models.Tasks.owner_id == current_user.id).first()

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Task with id {id} not found")

    db.delete(task)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update a task
@router.put("/{id}", response_model=schemas.Task)
async def update_task(id: int, updated_task: schemas.TaskUpdate, db: Session = Depends(get_db),
                      current_user: int = Depends(oauth2.get_current_user)):
    task = db.query(models.Tasks).filter(models.Tasks.id == id, models.Tasks.owner_id == current_user.id).first()

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Task with id {id} not found")

    for key, value in updated_task.model_dump(exclude_unset=True).items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task
