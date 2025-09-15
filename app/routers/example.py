from fastapi import APIRouter, Depends, HTTPException, Path, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.utils import get_lang

from .. import schemas, models, database

router = APIRouter(prefix="/example", tags=["example"])

# CREATE
@router.post("/", response_model=schemas.Example)
async def create(
    article: schemas.ExampleCreate, 
    db: AsyncSession = Depends(database.get_db)
):
    user_id = 123 # ToDo: Get real user ID.

    db_example = models.Example(**article.model_dump())
    db_example.user_id = user_id
    db.add(db_example)

    await db.commit()
    await db.refresh(db_example)

    return db_example

# READ ALL
@router.get("/", response_model=List[schemas.Example])
async def read_all(db: AsyncSession = Depends(database.get_db)):
    user_id = 123 # ToDo: Get real user ID.

    result = await db.execute(select(models.Example).where(models.Example.user_id == user_id))

    return result.scalars().all()

# READ
@router.get("/{id}", response_model=schemas.Example)
async def read(id: int = Path(...), db: AsyncSession = Depends(database.get_db)):
    user_id = 123  # ToDo: Get real user ID.
    
    result = await db.execute(
        select(models.Example)
        .where(models.Example.id == id)
        .where(models.Example.user_id == user_id)
    )
    db_example = result.scalar_one_or_none()
    
    if not db_example:
        raise HTTPException(status_code=404, detail="Example not found")
    
    return db_example

# UPDATE
@router.put("/{id}", response_model=schemas.Example)
async def update(
    id: int = Path(...), 
    example: schemas.ExampleUpdate = None,
    db: AsyncSession = Depends(database.get_db)
):
    user_id = 123 # ToDo: Get real user ID.
    
    db_example = await db.get(models.Example, id)
    if not db_example:
        raise HTTPException(status_code=404, detail="Example not found")
    
    for key, value in example.model_dump(exclude_unset=True).items():
        setattr(db_example, key, value)

    await db.commit()
    await db.refresh(db_example)

    return db_example

# DELETE
@router.delete("/{id}", response_model=schemas.Example)
async def delete(id: int = Path(...), db: AsyncSession = Depends(database.get_db)):
    user_id = 123 # ToDo: Get real user ID.

    db_example = await db.get(models.Example, id)
    if not db_example:
        raise HTTPException(status_code=404, detail="Example not found")
    
    await db.delete(db_example)
    await db.commit()

    return db_example

# DELETE ALL
@router.delete("/", response_model=List[schemas.Example])
async def delete_all(db: AsyncSession = Depends(database.get_db)):
    user_id = 123  # TODO: get real user ID

    result = await db.execute(
        select(models.Example).where(models.Example.user_id == user_id)
    )
    db_examples = result.scalars().all()

    if not db_examples:
        raise HTTPException(status_code=404, detail="No examples found")

    for example in db_examples:
        await db.delete(example)
    await db.commit()

    return db_examples
