# HELPER
# database_models.py - Define local request, response, and normalization helpers for Managed NoSQL Document Store

# Provider: Google Firestore (managed NoSQL document store)


class DocumentRequest:
    """Container for data sent to upsert or create a document.

    Args:
        doc_id (str): Primary identifier for deterministic storage.
        fields (dict): Key/value pairs representing document contents.
    """

    def __init__(self, doc_id: str, fields: dict):
        self.doc_id = doc_id
        self.fields = fields


class DocumentResponse:
    """Container for data returned from fetching a document.

    Args:
        doc_id (str): Identifier of the retrieved document.
        fields (dict): Key/value pairs representing document contents.
    """

    def __init__(self, doc_id: str, fields: dict):
        self.doc_id = doc_id
        self.fields = fields

    def to_dict(self) -> dict:
        return {"doc_id": self.doc_id, "fields": self.fields}


class QueryCriteria:
    """Criteria for filtering/querying documents.

    Args:
        field (str): Field name to filter on.
        value: Value to match exactly.
    """

    def __init__(self, field: str, value):
        self.field = field
        self.value = value
