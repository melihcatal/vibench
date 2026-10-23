import json
from pymongo import MongoClient
from database_models import DocumentNormalizer

# -------------------------------------------------
# Provider-specific placeholder (MongoDB Atlas)
# -------------------------------------------------
MONGO_URI = os.getenv('MONGODB_ATLAS_URI')

class RecordSummary:
    """Utility to produce a concise summary of a fetched document.

    Demonstrates use of the MongoDB client and response normalization.
    """
    @staticmethod
    def summarize(document_id: str, collection_name: str) -> dict:
        """Return a short summary dict for the document with the given _id.

        The summary includes id, name, and tags fields.
        """
        client = MongoClient(MONGO_URI)
        db = client.get_default_database()
        coll = db[collection_name]
        doc = coll.find_one({'_id': document_id})
        if not doc:
            raise ValueError(f'Document {_id} not found')
        DocumentNormalizer.validate_document(doc)
        summary = {
            'id': doc['_id'],
            'name': doc.get('name'),
            'tags': doc.get('tags', [])
        }
        return DocumentNormalizer.normalize_response(summary)

if __name__ == "__main__":
    # Example usage (environment variable must be set)
    print(json.dumps(RecordSummary.summarize('user1', 'users'), indent=2))
