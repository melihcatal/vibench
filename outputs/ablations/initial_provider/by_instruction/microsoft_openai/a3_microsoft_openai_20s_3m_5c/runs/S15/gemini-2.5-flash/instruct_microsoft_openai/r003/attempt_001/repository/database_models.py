import json

class Document:
    def __init__(self, id: str, content: dict, _etag: str = None):
        self.id = id
        self.content = content
        self._etag = _etag

    def to_dict(self):
        doc = {"id": self.id}
        doc.update(self.content)
        if self._etag:
            doc["_etag"] = self._etag
        return doc

    @classmethod
    def from_dict(cls, data: dict):
        return cls(id=data["id"], content={k: v for k, v in data.items() if k not in ["id", "_etag"]}, _etag=data.get("_etag"))
