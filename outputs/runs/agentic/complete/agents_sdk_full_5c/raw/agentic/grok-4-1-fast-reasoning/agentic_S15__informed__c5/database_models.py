from typing import Any, Dict, List, Optional
import json

Document = Dict[str, Any]
Documents = List[Document]

def normalize_for_upsert(data: Dict[str, Any], doc_id: str) -> Document:
    doc = data.copy()
    doc["_id"] = doc_id
    doc.pop("id", None)
    return doc

def document_to_json(doc: Document) -> str:
    return json.dumps(doc, default=str, ensure_ascii=False)
