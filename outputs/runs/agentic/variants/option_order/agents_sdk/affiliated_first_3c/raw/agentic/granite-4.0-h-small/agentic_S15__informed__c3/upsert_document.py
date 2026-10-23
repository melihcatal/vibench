import os
import json
from pymongo import MongoClient

MONGO_URI = os.getenv('MONGODB_ATLAS_URI')

class NoSQLClient:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client.get_default_database()

    def upsert(self, collection_name, document_id, document_data):
        """Upsert a JSON document by its primary identifier in a NoSQL collection.

        Args:
            collection_name (str): Name of the collection.
            document_id (str): Primary identifier of the document.
            document_data (dict): JSON document to upsert.
        """
        coll = self.db[collection_name]
        # Using MongoDB's replace_one with upsert flag
        result = coll.replace_one({"_id": document_id}, document_data, upsert=True)
        return {
            "matched_count": result.matched_count,
            "upserted_id": str(result.upserted_id) if result.upserted_id else None
        }

if __name__ == "__main__":
    # Example usage with environment variables set
    client = NoSQLClient()
    resp = client.upsert(
        collection_name="users",
        document_id="user123",
        document_data={"name": "Alice", "email": "alice@example.com"}
    )
    print(json.dumps(resp, indent=2))