from typing import Any, Dict


class DocumentRequest:
    def __init__(self, image_path: str):
        self.image_path = image_path


class DocumentResponse:
    def __init__(self, data: Dict[str, Any]):
        self.data = data

    def normalize(self):
        return self.data
