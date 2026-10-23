import json

class Document:
    def __init__(self, id, content, type="general"):
        self.id = id
        self.content = content
        self.type = type

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "type": self.type
        }

    @staticmethod
    def from_dict(data):
        return Document(data["id"], data["content"], data.get("type", "general"))
