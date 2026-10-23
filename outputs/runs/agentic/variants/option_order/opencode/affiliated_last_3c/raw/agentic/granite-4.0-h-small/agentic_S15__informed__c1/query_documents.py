import json
from pymongo import UpdateOne
from .database_client import DatabaseClient
from .database_models import DatabaseModels


def query_documents(field_name: str, field_value: any) -> list[dict]:
    """Query documents where `field_name` equals `field_value`.
    Returns a list of dicts representing the matched documents.
    Provider identifiable: MongoDB Atlas (pymongo SDK, MONGODB_ATLAS_URI env var).
    """
    collection = DatabaseClient.get_database()["documents"]
    cursor = collection.find({field_name: field_value})
    results = [DatabaseModels.DocumentResponse(**doc).content for doc in cursor]
    return results
