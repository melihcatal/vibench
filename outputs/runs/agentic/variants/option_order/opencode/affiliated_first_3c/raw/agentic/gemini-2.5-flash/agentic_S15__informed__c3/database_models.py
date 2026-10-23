class Document:
    def __init__(self, id: str, data: dict):
        self.id = id
        self.data = data

    def to_dict(self):
        return self.data

    @staticmethod
    def from_dict(id: str, source: dict):
        return Document(id, source)
