from app.items.exceptions import ItemNotFoundError
from app.items.repository import InMemoryItemRepository
from app.items.schemas import ItemCreate, ItemRead, ItemUpdate


class ItemService:
    """Business logic for items. Knows nothing about HTTP or storage details."""

    def __init__(self, repository: InMemoryItemRepository) -> None:
        self.repository = repository

    def list_items(self) -> list[ItemRead]:
        return self.repository.list()

    def get_item(self, item_id: int) -> ItemRead:
        item = self.repository.get(item_id)
        if item is None:
            raise ItemNotFoundError(item_id)
        return item

    def create_item(self, data: ItemCreate) -> ItemRead:
        return self.repository.add(data)

    def update_item(self, item_id: int, data: ItemUpdate) -> ItemRead:
        item = self.repository.update(item_id, data)
        if item is None:
            raise ItemNotFoundError(item_id)
        return item

    def delete_item(self, item_id: int) -> None:
        if not self.repository.delete(item_id):
            raise ItemNotFoundError(item_id)
