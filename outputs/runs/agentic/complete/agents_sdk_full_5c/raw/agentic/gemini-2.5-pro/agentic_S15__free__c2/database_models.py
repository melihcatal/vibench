from typing import Dict, Any

class Document:
    """
    A simple class representing the structure of a document.
    This can be expanded with more validation or methods as needed.
    """
    def __init__(self, document_id: str, content: str, author: str, version: int = 1):
        self.document_id = document_id
        self.content = content
        self.author = author
        self.version = version

    def to_dynamodb_item(self) -> Dict[str, Any]:
        """
        Serializes the document object into a DynamoDB item format.
        """
        return {
            'documentId': {'S': self.document_id},
            'content': {'S': self.content},
            'author': {'S': self.author},
            'version': {'N': str(self.version)}
        }

    @staticmethod
    def from_dynamodb_item(item: Dict[str, Any]) -> 'Document':
        """
        Deserializes a DynamoDB item into a Document object.
        """
        return Document(
            document_id=item['documentId']['S'],
            content=item['content']['S'],
            author=item['author']['S'],
            version=int(item['version']['N'])
        )
