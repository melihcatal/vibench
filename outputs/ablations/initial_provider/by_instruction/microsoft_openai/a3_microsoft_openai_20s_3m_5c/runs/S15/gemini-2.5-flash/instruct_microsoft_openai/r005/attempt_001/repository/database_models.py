from typing import Dict, Any

class Document:
    def __init__(self, id: str, content: Dict[str, Any]):
        self.id = id
        self.content = content

    def to_dict(self):
        return {"id": self.id, **self.content}
