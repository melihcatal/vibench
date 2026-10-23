class Document:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    @staticmethod
    def from_dict(data):
        return Document(**data)