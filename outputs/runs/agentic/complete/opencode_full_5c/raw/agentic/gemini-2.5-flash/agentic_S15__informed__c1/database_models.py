class Document:
    def __init__(self, id, data):
        self.id = id
        self.data = data

    def to_dict(self):
        return self.data

    @staticmethod
    def from_dict(source):
        return Document(source.id, source.to_dict())
