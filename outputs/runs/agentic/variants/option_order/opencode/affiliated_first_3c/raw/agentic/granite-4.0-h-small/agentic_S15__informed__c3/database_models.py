class DatabaseModels:
    """Normalization helpers for request and response payloads when using the Managed NoSQL Document Store."""

    @staticmethod
    def normalize_upsert(payload):
        # Ensure primary identifier field is present
        if "_id" not in payload:
            raise ValueError("Payload must contain _id field")
        return payload

    @staticmethod
    def normalize_fetch(doc_id):
        return {"_id": doc_id}

    @staticmethod
    def normalize_query(filters):
        # Simple key/value filters for query_documents.py
        return filters

    @staticmethod
    def normalize_conditional_update(doc_id, update, version):
        update["_id"] = doc_id
        update["_rev"] = version
        return update
