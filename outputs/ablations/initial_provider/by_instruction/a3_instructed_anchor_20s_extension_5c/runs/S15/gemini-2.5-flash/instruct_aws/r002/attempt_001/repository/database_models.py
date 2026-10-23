from typing import Dict, Any

class Document:
    """
    Represents a generic document structure for the NoSQL store.
    """
    def __init__(self, document_id: str, content: Dict[str, Any]):
        self.document_id = document_id
        self.content = content

    def to_item(self) -> Dict[str, Any]:
        """
        Converts the document to a DynamoDB item format.
        """
        item = {
            "document_id": {"S": self.document_id},
        }
        for key, value in self.content.items():
            if isinstance(value, str):
                item[key] = {"S": value}
            elif isinstance(value, int):
                item[key] = {"N": str(value)}
            elif isinstance(value, bool):
                item[key] = {"BOOL": value}
            # Add more type handling as needed
        return item

    @staticmethod
    def from_item(item: Dict[str, Any]):
        """
        Converts a DynamoDB item to a Document object.
        """
        document_id = item["document_id"]["S"]
        content = {}
        for key, value in item.items():
            if key == "document_id":
                continue
            if "S" in value:
                content[key] = value["S"]
            elif "N" in value:
                content[key] = int(value["N"])
            elif "BOOL" in value:
                content[key] = value["BOOL"]
            # Add more type handling as needed
        return Document(document_id, content)
