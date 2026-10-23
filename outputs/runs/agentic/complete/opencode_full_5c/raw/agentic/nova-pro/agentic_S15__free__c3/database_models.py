class Document:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def to_dict(self):
        return self.__dict__.copy()
