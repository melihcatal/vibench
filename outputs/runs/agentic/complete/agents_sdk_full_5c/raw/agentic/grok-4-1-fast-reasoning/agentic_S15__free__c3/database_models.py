from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class Document:
    id: str
    data: Dict[str, Any]
    version: int

def document_from_item(item: Dict[str, Any]) -> Document:
    return Document(
        id=item['id'],
        data=item['data'],
        version=item.get('version', 0)
    )

def documents_from_items(items: List[Dict[str, Any]]) -> List[Document]:
    return [document_from_item(item) for item in items]

def item_from_document(doc: Document) -> Dict[str, Any]:
    return {
        'id': doc.id,
        'data': doc.data,
        'version': doc.version
    }
