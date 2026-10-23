class Document:
    def __init__(self, id, name, value):
        self.id = id
        self.name = name
        self.value = value

    @staticmethod
    def from_dict(dict):
        return Document(dict["id"], dict["name"], dict["value"])
