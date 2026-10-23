from typing import Dict, Any, List

def document_payload(doc_id: str, document: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": doc_id,
        "document": document
    }

def query_payload(collection: str, field: str, value: Any) -> Dict[str, Any]:
    return {
        "collection": collection,
        "field": field,
        "value": value
    }

def update_payload(doc_id: str, updates: Dict[str, Any], condition_field: str = None, condition_value: Any = None) -> Dict[str, Any]:
    payload = {
        "id": doc_id,
        "updates": updates
    }
    if condition_field and condition_value:
        payload["condition_field"] = condition_field
        payload["condition_value"] = condition_value
    return payload
