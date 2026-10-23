from typing import Dict, Any, Optional


class Document:
    def __init__(self, document_id: str, data: Dict[str, Any]):
        self.document_id = document_id
        self.data = data

    def to_dynamodb_item(self) -> Dict[str, Any]:
        item = {"id": {"S": self.document_id}}
        for key, value in self.data.items():
            if isinstance(value, str):
                item[key] = {"S": value}
            elif isinstance(value, (int, float)):
                item[key] = {"N": str(value)}
            elif isinstance(value, bool):
                item[key] = {"BOOL": value}
            elif isinstance(value, list):
                # Simple list of strings or numbers
                item[key] = {"L": [{"S": str(v)} for v in value]}
            else:
                # Treat as string for simplicity or raise error
                item[key] = {"S": str(value)}
        return item

    @staticmethod
    def from_dynamodb_item(item: Dict[str, Any]) -> Optional["Document"]:
        if not item or "id" not in item or "S" not in item["id"]:
            return None

        document_id = item["id"]["S"]
        data = {}
        for key, value_obj in item.items():
            if key == "id":
                continue
            if "S" in value_obj:
                data[key] = value_obj["S"]
            elif "N" in value_obj:
                data[key] = float(value_obj["N"])  # DynamoDB stores numbers as strings
            elif "BOOL" in value_obj:
                data[key] = value_obj["BOOL"]
            elif "L" in value_obj:
                data[key] = [
                    v["S"] for v in value_obj["L"]
                ]  # Assuming list of strings for simplicity
            # Add more type handling as needed
        return Document(document_id, data)
