import json

class DocumentNormalizer:
    """Helper utilities to normalize request/response payloads for a NoSQL document store.

    Provides methods for basic validation and transformation.
    """
    @staticmethod
    def validate_document(doc):
        if not isinstance(doc, dict):
            raise ValueError('Document must be a dict')
        # Example: ensure _id field exists for upserts
        if '_id' not in doc:
            raise ValueError('_id field is required')

    @staticmethod
    def normalize_response(doc):
        """Convert a raw BSON document to a plain JSON dict (if needed)."""
        return json.loads(json.dumps(doc))  # shallow conversion

if __name__ == "__main__":
    # Example usage
    doc = {'_id': 'doc1', 'name': 'Test', 'tags': ['a', 'b']}
    DocumentNormalizer.validate_document(doc)
    print('Normalized:', DocumentNormalizer.normalize_response(doc))
