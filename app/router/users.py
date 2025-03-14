from fastapi import APIRouter, Depends, Response, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import models, schemas, utils, oauth2

router = APIRouter(tags=['User'])


@router.post("/create_user", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
async def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    user.password = utils.hash(user.password)  # Hash password before storing
    new_user = models.Users(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/users", response_model=List[schemas.User])
async def read_users(db: Session = Depends(get_db)):
    return db.query(models.Users).all()


@router.delete("/user", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(db: Session = Depends(get_db), current_user: models.Users = Depends(oauth2.get_current_user)):
    user = db.query(models.Users).filter(models.Users.id == current_user.id)
    if user.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/user", response_model=schemas.User)
async def update_user(schema: schemas.CreateUser, db: Session = Depends(get_db),
                      current_user: models.Users = Depends(oauth2.get_current_user)):
    user = db.query(models.Users).filter(models.Users.id == current_user.id)
    if user.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if schema.password:
        schema.password = utils.hash(schema.password)  # Hash new password before updating

    user.update(schema.model_dump(), synchronize_session=False)
    db.commit()
    return user.first()
