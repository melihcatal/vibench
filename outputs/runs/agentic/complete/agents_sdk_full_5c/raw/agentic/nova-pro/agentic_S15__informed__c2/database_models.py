class DynamoDBModel:
    def __init__(self, table_name):
        self.table_name = table_name

    def normalize_item(self, item):
        return {k: {'S': v} for k, v in item.items()}