import json
from typing import Dict, Any, List
from database_models import DocumentResponse


def summarize_record(doc: DocumentResponse) -> Dict[str, Any]:
    """
    Produces a concise summary of a fetched document.
    Includes key identifiers and a short preview of top-level fields.
    """
    summary = {"id": doc.id, "type": doc.data.get("type", "unknown"), "preview": {}}
    # Capture first few non‑empty string/number fields for preview
    for k, v in doc.data.items():
        if isinstance(v, (str, int, float)) and k not in ("id", "type"):
            summary["preview"][k] = str(v)[:50] + ("..." if len(str(v)) > 50 else "")
            if len(summary["preview"]) >= 5:
                break  # limit to first five preview fields
    return summary


# Example CLI to test summarization
if __name__ == "__main__":
    sample_doc = {
        "id": "demo-001",
        "data": {
            "type": "note",
            "title": "Sample Note",
            "content": "This is a longer content that goes beyond the preview limit.",
            "created_at": "2025-01-01T12:00:00Z",
            "tags": ["demo", "example"],
        },
    }
    doc = DocumentResponse(**sample_doc)
    print(json.dumps(summarize_record(doc), indent=2))
