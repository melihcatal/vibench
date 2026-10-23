import os
import json
from pymongo import MongoClient
from database_client import NoSQLClient
from database_models import DocumentNormalizer

# -------------------------------------------------
# Provider configuration (MongoDB Atlas)
# -------------------------------------------------
MONGO_URI = os.getenv('MONGODB_ATLAS_URI')

class QueryDocuments:
    """Query multiple documents by a field value or partition-style key.

    Uses MongoDB find with optional filter criteria.
    """
    @staticmethod
    def query(collection_name: str, filter_criteria: dict) -> list:
        """
        Return a list of documents matching filter_criteria.

        Args:
            collection_name (str): Target collection.
            filter_criteria (dict): Query filter (e.g., {'tags': 'beta', 'status': {'$ne': 'inactive'}}).

        Returns:
            list: Normalized JSON documents.
        """
        coll = NoSQLClient().db[collection_name]
        cursor = coll.find(filter_criteria)
        results = [DocumentNormalizer.normalize_response(doc) for doc in cursor]
        return results

if __name__ == "__main__":
    # Example usage (environment variable must be set)
    results = QueryDocuments.query(
        collection_name='users',
        filter_criteria={'status': 'active', 'country': 'US'}
    )
    print(json.dumps(results, indent=2))
