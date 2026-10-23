class Document:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    @classmethod
    def from_dynamodb(cls, item):
        return cls(**item)

    def to_dynamodb(self):
        return self.__dict__
