class Document:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    @staticmethod
    def from_dict(d):
        return Document(**d)

    def to_dict(self):
        return self.__dict__