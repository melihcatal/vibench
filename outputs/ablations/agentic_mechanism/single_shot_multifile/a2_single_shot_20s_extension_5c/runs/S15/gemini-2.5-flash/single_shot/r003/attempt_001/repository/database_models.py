from typing import Dict, Any, List

DocumentKey = Dict[str, Any]
DocumentItem = Dict[str, Any]

def normalize_document(document: DocumentItem) -> DocumentItem:
    return document

def serialize_for_db(document: DocumentItem) -> DocumentItem:
    for k, v in document.items():
        if isinstance(v, (list, dict)):
            document[k] = str(v)
    return document

def deserialize_from_db(item: DocumentItem) -> DocumentItem:
    return item