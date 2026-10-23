import json


class Document:
    """
    A simple model for a document in the NoSQL store.
    """

    def __init__(self, id: str, data: dict):
        self.id = id
        self.data = data

    def to_json(self):
        return json.dumps({"id": self.id, "data": self.data})

    @staticmethod
    def from_json(json_string: str):
        parsed = json.loads(json_string)
        return Document(parsed["id"], parsed["data"])

    def to_dynamodb_item(self):
        """Converts the Document object to a DynamoDB item format."""
        item = {"id": {"S": self.id}}
        for key, value in self.data.items():
            # Simple type mapping, extend as needed for more complex types
            if isinstance(value, str):
                item[key] = {"S": value}
            elif isinstance(value, int):
                item[key] = {"N": str(value)}
            elif isinstance(value, bool):
                item[key] = {"BOOL": value}
            elif isinstance(value, list):
                item[key] = {"L": [{"S": v} for v in value]}  # Assuming list of strings
            elif isinstance(value, dict):
                item[key] = {
                    "M": {k: {"S": v} for k, v in value.items()}
                }  # Assuming dict of strings
            else:
                item[key] = {"S": str(value)}  # Default to string
        return item

    @staticmethod
    def from_dynamodb_item(item: dict):
        """Converts a DynamoDB item format to a Document object."""
        doc_id = item["id"]["S"]
        data = {}
        for key, value_obj in item.items():
            if key == "id":
                continue
            if "S" in value_obj:
                data[key] = value_obj["S"]
            elif "N" in value_obj:
                data[key] = int(value_obj["N"])
            elif "BOOL" in value_obj:
                data[key] = value_obj["BOOL"]
            elif "L" in value_obj:
                data[key] = [v["S"] for v in value_obj["L"]]
            elif "M" in value_obj:
                data[key] = {k: v["S"] for k, v in value_obj["M"].items()}
        return Document(doc_id, data)
