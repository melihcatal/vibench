from typing import Dict


class Document:
    def __init__(self, id: str, data: Dict):
        self.id = id
        self.data = data
