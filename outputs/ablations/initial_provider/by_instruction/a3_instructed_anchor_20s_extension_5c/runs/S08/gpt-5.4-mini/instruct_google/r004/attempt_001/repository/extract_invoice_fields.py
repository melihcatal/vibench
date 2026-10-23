import json
import os
from typing import Any, Dict, List

from google.cloud import documentai

from document_client import get_client, load_config, process_content


def _entity_map(document: Any) -> Dict[str, List[Dict[str, Any]]]:
    mapped: Dict[str, List[Dict[str, Any]]] = {}
    for entity in getattr(document, "entities", []):
        mapped.setdefault(getattr(entity, "type_", ""), []).append(
            {
                "text": getattr(entity, "mention_text", ""),
                "confidence": float(getattr(entity, "confidence", 0.0) or 0.0),
            }
        )
    return mapped


def extract_invoice_fields(content: bytes, mime_type: str = "application/pdf") -> Dict[str, Any]:
    config = load_config()
    client = get_client()
    document = process_content(client, config, content, mime_type)
    entities = _entity_map(document)
    return {
        "vendor": entities.get("vendor", [{}])[0].get("text", ""),
        "date": entities.get("invoice_date", [{}])[0].get("text", ""),
        "total": entities.get("total_amount", [{}])[0].get("text", ""),
        "line_items": entities.get("line_item", []),
        "provider": "google-cloud-documentai",
    }


def main() -> None:
    path = os.environ.get("DOCUMENT_PATH", "")
    if not path:
        raise SystemExit(1)
    with open(path, "rb") as fh:
        result = extract_invoice_fields(fh.read())
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
