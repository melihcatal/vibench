# [HELPER] database_models.py
# Local request/response and normalization helpers for DynamoDB NoSQL store


class DocumentRequest:
    """Helper class for building document upsert payloads."""

    def __init__(self, primary_id, fields):
        """Args:
        primary_id (str): Document identifier (partition key).
        fields (dict): Additional key/value pairs to store.
        """
        self.primary_id = primary_id
        self.fields = fields

    def to_dynamodb_item(self):
        return {"id": {"S": str(self.primary_id)}, **self.fields}


class DocumentResponse:
    """Wrapper for a fetched DynamoDB document."""

    def __init__(self, data):
        # Expect data as dict of {'S': value} pairs
        self.data = data

    def to_dict(self):
        return {k: v["S"] for k, v in self.data.items()}


class QueryResult(list):
    """List-like container for multiple fetched documents."""

    def __init__(self, items):
        # Each item is expected to be a dict of DynamoDB attribute dicts
        super().__init__(items)

    def to_list_of_dicts(self):
        return [self.to_dict(item) for item in self]

    @staticmethod
    def to_dict(item):
        return {k: v["S"] for k, v in item.items()}


# Usage examples (local testing only):
# req = DocumentRequest('doc1', {'name': 'Bob', 'age': 25})
# item = req.to_dynamodb_item()
# resp = DocumentResponse(item)
# print(resp.to_dict())
