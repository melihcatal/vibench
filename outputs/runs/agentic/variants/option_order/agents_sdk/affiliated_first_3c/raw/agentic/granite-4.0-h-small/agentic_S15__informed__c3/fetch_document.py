import os
import json
from pymongo import MongoClient
from database_client import NoSQLClient
from database_models import DocumentNormalizer

# -------------------------------------------------
# Provider configuration (MongoDB Atlas)
# -------------------------------------------------
MONGO_URI = os.getenv('MONGODB_ATLAS_URI')

class FetchDocument:
    """Fetch a single document by its primary identifier from a NoSQL collection.

    Demonstrates use of the NoSQLClient helper and response normalization.
    """
    @staticmethod
    def fetch_one(collection_name: str, document_id: str) -> dict:
        """
        Retrieve a document by _id.

        Args:
            collection_name (str): Name of the MongoDB collection.
            document_id (str): The value of the _id field to locate.

        Returns:
            dict: Normalized JSON document, or raises ValueError if not found.
        """
        coll = NoSQLClient().db[collection_name]
        doc = coll.find_one({'_id': document_id})
        if not doc:
            raise ValueError(f'Document with id {document_id} not found')
        DocumentNormalizer.validate_document(doc)
        return DocumentNormalizer.normalize_response(doc)

if __name__ == "__main__":
    # Example usage (environment variable must be set)
    doc = FetchDocument.fetch_one('users', 'user123')
    print(json.dumps(doc, indent=2))
