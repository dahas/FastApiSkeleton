import json
from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app import database, models
from app.api.v1 import schemas
from app.utils import get_current_user

router = APIRouter(prefix="/example", tags=["example"])

# CREATE
@router.post("/", response_model=schemas.Example, status_code=status.HTTP_201_CREATED)
async def create(
    article: schemas.ExampleCreate, 
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    user_id = current_user.id

    row = models.Example(**article.model_dump())
    row.user_id = user_id
    db.add(row)

    await db.commit()
    await db.refresh(row)

    return row

# READ ALL
@router.get("/", response_model=List[schemas.Example], status_code=status.HTTP_200_OK)
async def read_all(
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    user_id = current_user.id

    result = await db.execute(select(models.Example).where(models.Example.user_id == user_id))

    rows = result.scalars().all()
    print(json.dumps([{"id": r.id, "title": r.title, "content": r.content} for r in rows], indent=2))

    return rows

# READ
@router.get("/{id}", response_model=schemas.Example, status_code=status.HTTP_200_OK)
async def read(
    id: int = Path(...), 
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    user_id = current_user.id
    
    result = await db.execute(
        select(models.Example)
        .where(models.Example.id == id)
        .where(models.Example.user_id == user_id)
    )
    row = result.scalar_one_or_none()
    
    if not row:
        raise HTTPException(status_code=404, detail="Example not found")
    
    print(json.dumps({"id": row.id, "title": row.title, "content": row.content}, indent=2))
    
    return row

# UPDATE
@router.put("/{id}", response_model=schemas.Example, status_code=status.HTTP_200_OK)
async def update(
    id: int = Path(...), 
    example: schemas.ExampleUpdate = None,
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    user_id = current_user.id

    result = await db.execute(
        select(models.Example)
        .where(models.Example.id == id)
        .where(models.Example.user_id == user_id)
    )
    row = result.scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="Example not found")
    
    for key, value in example.model_dump(exclude_unset=True).items():
        setattr(row, key, value)

    await db.commit()
    await db.refresh(row)

    print(json.dumps({"id": row.id, "title": row.title, "content": row.content}, indent=2))

    return row

# DELETE
@router.delete("/{id}", response_model=schemas.Example, status_code=status.HTTP_200_OK)
async def delete(
    id: int = Path(...), 
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    user_id = current_user.id

    result = await db.execute(
        select(models.Example)
        .where(models.Example.id == id)
        .where(models.Example.user_id == user_id)
    )
    row = result.scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="Example not found")
    
    await db.delete(row)
    await db.commit()

    return row

# DELETE ALL
@router.delete("/", response_model=List[schemas.Example], status_code=status.HTTP_200_OK)
async def delete_all(
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    user_id = current_user.id

    result = await db.execute(
        select(models.Example).where(models.Example.user_id == user_id)
    )
    rows = result.scalars().all()

    if not rows:
        raise HTTPException(status_code=404, detail="No examples found")

    for example in rows:
        await db.delete(example)
    await db.commit()

    return rows
