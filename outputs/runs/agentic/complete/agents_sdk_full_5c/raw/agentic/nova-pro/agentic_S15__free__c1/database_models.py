class DynamoDBItem:
    def __init__(self, **kwargs):
        self.attributes = kwargs

    def to_dict(self):
        return self.attributes