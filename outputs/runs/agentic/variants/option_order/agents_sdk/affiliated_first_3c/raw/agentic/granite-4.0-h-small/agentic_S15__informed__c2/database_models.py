import json

def normalize_document(doc):
    """Normalize a document dict to ensure required keys exist and types are consistent."""
    # Ensure basic fields are strings/numbers
    if not isinstance(doc, dict):
        raise ValueError("Document must be a dictionary")
    normalized = {
        "id": str(doc.get("id", "<missing-id>")),
        "name": str(doc.get("name", "<no-name>")),
        "created_at": doc.get("created_at")
    }
    # Add any other fields you need to normalize
    return normalized

# Example helper used by same-scenario files
if __name__ == "__main__":
    raw = {
        "id": 123,
        "name": "Example",
        "created_at": "2025-08-15T12:00:00Z"
    }
    print("Normalized document:", json.dumps(normalize_document(raw), indent=2))
