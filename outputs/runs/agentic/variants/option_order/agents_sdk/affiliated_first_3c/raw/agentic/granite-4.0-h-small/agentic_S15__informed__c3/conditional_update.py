import os
import json
from pymongo import MongoClient
from database_models import DocumentNormalizer

class ConditionalUpdater:
    """Applies a version‑aware (optimistic) update to a document in a managed NoSQL store.

    Uses MongoDB's findAndModify with a $inc version guard.
    """
    MONGO_URI = os.getenv('MONGODB_ATLAS_URI')

    @staticmethod
    def update_if_version_matches(collection_name: str, document_id: str, expected_version: int, update_spec: dict) -> dict:
        """
        Update a document only if its stored version matches expected_version.

        Args:
            collection_name (str): Collection containing the document.
            document_id (str): _id of the document.
            expected_version (int): Version value stored under the field '_version'.
            update_spec (dict): Update operations (e.g., {'$set': {'status': 'active'}}).

        Returns:
            dict: JSON with matched, modified counts and new version, or an error message.
        """
        client = MongoClient(ConditionalUpdater.MONGO_URI)
        db = client.get_default_database()
        coll = db[collection_name]
        coll.create_index([('id', 1)], name='unique_id')  # ensure _id uniqueness

        result = coll.find_one_and_update(
            {'_id': document_id, '_version': expected_version},
            {'$inc': {'_version': 1}, '$set': update_spec},
            return_document=True,
        )

        if result is None:
            return {'status': 'not_updated', 'reason': 'version mismatch or document missing'}
        return {
            'status': 'updated',
            'matched_count': 1,
            'modified_count': 1,
            'new_version': result['_version'],
            'updated_document': DocumentNormalizer.normalize_response(result)
        }

if __name__ == "__main__":
    # Example usage (environment variable must be set)
    result = ConditionalUpdater.update_if_version_matches(
        collection_name='users',
        document_id='user123',
        expected_version=2,
        update_spec={'$set': {'status': 'active'}}
    )
    print(json.dumps(result, indent=2))
