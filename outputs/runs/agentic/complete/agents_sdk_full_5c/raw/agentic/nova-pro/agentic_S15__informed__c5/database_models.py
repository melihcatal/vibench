class Document:
    def __init__(self, id, field):
        self.id = id
        self.field = field

    def to_dict(self):
        return {'id': self.id, 'field': self.field}