from app.items.schemas import ItemCreate, ItemRead, ItemUpdate


class InMemoryItemRepository:
    """Stores items in a dict. Data is lost when the server restarts.

    To use a real database, write a class with the same methods
    and return it from `get_item_repository` in dependencies.py.
    Nothing else needs to change.
    """

    def __init__(self) -> None:
        self._items: dict[int, ItemRead] = {}
        self._next_id = 1

    def list(self) -> list[ItemRead]:
        return list(self._items.values())

    def get(self, item_id: int) -> ItemRead | None:
        return self._items.get(item_id)

    def add(self, data: ItemCreate) -> ItemRead:
        item = ItemRead(id=self._next_id, **data.model_dump())
        self._items[item.id] = item
        self._next_id += 1
        return item

    def update(self, item_id: int, data: ItemUpdate) -> ItemRead | None:
        if item_id not in self._items:
            return None
        item = ItemRead(id=item_id, **data.model_dump())
        self._items[item_id] = item
        return item

    def delete(self, item_id: int) -> bool:
        return self._items.pop(item_id, None) is not None
