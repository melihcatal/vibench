class Document:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def to_dict(self):
        return {'id': self.id, 'name': self.name}

    @staticmethod
    def from_dict(data):
        return Document(data['id'], data['name'])