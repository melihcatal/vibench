from typing import Dict, Any, Optional, List

def prepare_document(doc_id: str, document: Dict[str, Any]) -> Dict[str, Any]:
    doc = document.copy()
    doc["_id"] = doc_id
    return doc

def parse_document(raw_doc: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    if raw_doc is None:
        return None
    doc = raw_doc.copy()
    doc.pop("_id", None)
    return doc

def parse_documents(raw_docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [parse_document(d) for d in raw_docs if d is not None]