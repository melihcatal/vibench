class Document:
    def __init__(self, id: str, content: dict):
        self.id = id
        self.content = content

    def to_item(self):
        item = {
            "id": {"S": self.id}
        }
        for key, value in self.content.items():
            item[key] = self._serialize_value(value)
        return item

    @staticmethod
    def from_item(item: dict):
        content = {}
        doc_id = item.get("id", {}).get("S")
        for key, value in item.items():
            if key != "id":
                content[key] = Document._deserialize_value(value)
        return Document(doc_id, content)

    @staticmethod
    def _serialize_value(value):
        if isinstance(value, str):
            return {"S": value}
        elif isinstance(value, (int, float)):
            return {"N": str(value)}
        elif isinstance(value, bool):
            return {"BOOL": value}
        elif isinstance(value, list):
            return {"L": [Document._serialize_value(v) for v in value]}
        elif isinstance(value, dict):
            return {"M": {k: Document._serialize_value(v) for k, v in value.items()}}
        elif value is None:
            return {"NULL": True}
        else:
            return {"S": str(value)} # Default to string for other types

    @staticmethod
    def _deserialize_value(value):
        if "S" in value:
            return value["S"]
        elif "N" in value:
            try:
                return int(value["N"])
            except ValueError:
                return float(value["N"])
        elif "BOOL" in value:
            return value["BOOL"]
        elif "L" in value:
            return [Document._deserialize_value(v) for v in value["L"]]
        elif "M" in value:
            return {k: Document._deserialize_value(v) for k, v in value["M"].items()}
        elif "NULL" in value:
            return None
        return value
