from __future__ import annotations
from typing import Any, Dict

# Local helper models for DynamoDB interaction

class Document:
    """Domain representation of a document stored in the NoSQL store."""
    def __init__(self, doc_id: str, title: str, content: str, version: str):
        self.doc_id = doc_id
        self.title = title
        self.content = content
        self.version = version

    @classmethod
    def from_dynamodb_item(cls, item: Dict[str, Any]) -> Document:
        """Convert raw DynamoDB item (dict) to Domain Document."""
        return cls(
            doc_id=item['id']['S'],
            title=item['title']['S'],
            content=item['content']['S'],
            version=item.get('version', {}).get('S', '')
        )

    def to_dict(self) -> Dict[str, Any]:
        """Transform Document into a DynamoDB item dictionary."""
        return {
            'id': {'S': self.doc_id},
            'title': {'S': self.title},
            'content': {'S': self.content},
            'version': {'S': self.version}
        }

# Simple payload parser for upserts
PARSE_MAP = {
    'id': str,
    'title': str,
    'content': str,
    'version': str
}

def parse_item(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and cast payload fields to DynamoDB attribute format."""
    out = {}
    for k, caster in PARSE_MAP.items():
        if k in payload:
            out[k] = { 'S': str(caster(payload[k])) }
    return out

if __name__ == "__main__":
    # Quick sanity test
    doc = Document('test-id', 'Test', 'Hello', '1')
    print('Parsed DynamoDB item:', parse_item(doc.to_dict()))
