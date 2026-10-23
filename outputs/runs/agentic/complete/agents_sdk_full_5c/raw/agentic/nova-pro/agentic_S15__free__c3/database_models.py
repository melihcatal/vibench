class DynamoDBItem:
    def __init__(self, **kwargs):
        self.item = {k: {'S': v} for k, v in kwargs.items()}