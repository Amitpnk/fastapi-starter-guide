from fastapi import APIRouter, status

from app.items.dependencies import ItemServiceDep
from app.items.schemas import ItemCreate, ItemRead, ItemUpdate

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=list[ItemRead])
def list_items(service: ItemServiceDep):
    return service.list_items()


@router.get("/{item_id}", response_model=ItemRead)
def get_item(item_id: int, service: ItemServiceDep):
    return service.get_item(item_id)


@router.post("", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def create_item(data: ItemCreate, service: ItemServiceDep):
    return service.create_item(data)


@router.put("/{item_id}", response_model=ItemRead)
def update_item(item_id: int, data: ItemUpdate, service: ItemServiceDep):
    return service.update_item(item_id, data)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, service: ItemServiceDep):
    service.delete_item(item_id)
