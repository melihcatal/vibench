from typing import Dict, Any

# A simple type alias for a document. In a more complex scenario,
# this could be a dataclass or a Pydantic model.
Document = Dict[str, Any]

# Helper to normalize document content if needed. For now, it's a passthrough.
def normalize_document_for_db(document: Document) -> Document:
    # Add any necessary normalization here before storing in the DB
    return document

def normalize_document_from_db(item: Dict[str, Any]) -> Document:
    # Add any necessary de-normalization or type conversion after fetching from DB
    return item
