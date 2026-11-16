class ItemNotFoundError(Exception):
    """Raised by the service when an item doesn't exist.

    The service doesn't know about HTTP; app/main.py turns this into a 404.
    """

    def __init__(self, item_id: int) -> None:
        self.item_id = item_id
        super().__init__(f"Item {item_id} not found")
