from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import src.crud as crud
from src.database import get_db
from src.auth import get_current_active_user

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=crud.Item)
def create_item(
    item: crud.ItemCreate,
    db: Session = Depends(get_db),
    current_user: crud.User = Depends(get_current_active_user)
):
    """
    Create a new item (requires authentication).
    - **title**: item title
    - **description**: optional description
    - **price**: item price
    """
    return crud.create_item(db=db, item=item)

@router.get("/", response_model=List[crud.Item])
def read_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get list of all items.
    - **skip**: number of records to skip
    - **limit**: maximum number of records to return
    """
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

@router.get("/{item_id}", response_model=crud.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    """
    Get a specific item by ID.
    """
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@router.put("/{item_id}", response_model=crud.Item)
def update_item(
    item_id: int,
    item: crud.ItemCreate,
    db: Session = Depends(get_db),
    current_user: crud.User = Depends(get_current_active_user)
):
    """
    Update an existing item (requires authentication).
    """
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Update fields
    db_item.title = item.title
    db_item.description = item.description
    db_item.price = item.price
    
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/{item_id}")
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: crud.User = Depends(get_current_active_user)
):
    """
    Delete an item (requires authentication).
    """
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted successfully"}