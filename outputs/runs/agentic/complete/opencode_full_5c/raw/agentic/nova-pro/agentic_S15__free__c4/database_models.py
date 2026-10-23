class Document:
    def __init__(self, id, data):
        self.id = id
        self.data = data

    @staticmethod
    def from_dict(d):
        return Document(d["id"], d["data"])
