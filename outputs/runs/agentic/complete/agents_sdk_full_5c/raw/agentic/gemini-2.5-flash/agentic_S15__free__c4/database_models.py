from typing import Dict, Any, Optional

class Document:
    """
    Represents a generic document structure.
    """
    def __init__(self, id: str, data: Dict[str, Any]):
        self.id = id
        self.data = data

    def to_item(self) -> Dict[str, Dict[str, Any]]:
        """
        Converts the document to a DynamoDB-compatible item.
        """
        item = {"id": {"S": self.id}}
        for key, value in self.data.items():
            # Simplified type mapping for demonstration
            if isinstance(value, str):
                item[key] = {"S": value}
            elif isinstance(value, (int, float)):
                item[key] = {"N": str(value)}
            elif isinstance(value, bool):
                item[key] = {"BOOL": value}
            elif isinstance(value, dict):
                # Further serialization needed for nested objects
                item[key] = {"S": str(value)} # Simplistic for now
            elif isinstance(value, list):
                # Further serialization needed for lists
                item[key] = {"S": str(value)} # Simplistic for now
            else:
                item[key] = {"S": str(value)}
        return item

    @staticmethod
    def from_item(item: Dict[str, Any]) -> Optional["Document"]:
        """
        Converts a DynamoDB item back to a Document object.
        """
        if not item or "id" not in item or "S" not in item["id"]:
            return None

        doc_id = item["id"]["S"]
        data = {}
        for key, value_obj in item.items():
            if key == "id":
                continue
            if "S" in value_obj:
                data[key] = value_obj["S"]
            elif "N" in value_obj:
                try:
                    data[key] = int(value_obj["N"])
                except ValueError:
                    data[key] = float(value_obj["N"])
            elif "BOOL" in value_obj:
                data[key] = value_obj["BOOL"]
            # Add more type handling as needed
        return Document(id=doc_id, data=data)

class DocumentUpdate:
    """
    Represents an update payload for a document.
    """
    def __init__(self, updates: Dict[str, Any], version: Optional[int] = None):
        self.updates = updates
        self.version = version
