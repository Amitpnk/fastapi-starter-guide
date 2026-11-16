from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from app.items.repository import InMemoryItemRepository
from app.items.service import ItemService


@lru_cache
def get_item_repository() -> InMemoryItemRepository:
    # lru_cache makes this return the same instance on every request,
    # so the in-memory data is shared. Tests override this function.
    return InMemoryItemRepository()


def get_item_service(
    repository: Annotated[InMemoryItemRepository, Depends(get_item_repository)],
) -> ItemService:
    return ItemService(repository)


ItemServiceDep = Annotated[ItemService, Depends(get_item_service)]
