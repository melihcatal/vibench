class DynamoDBItem:
    def __init__(self, item):
        self.item = item

    def to_dict(self):
        return self.item