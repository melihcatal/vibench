import json
from pymongo import ReadPreference, errors
from .database_client import DatabaseClient
from .database_models import DatabaseModels


def fetch_document(identifier: str) -> dict:
    """Fetch a single document by its identifier from the collection.
    Returns a dict representing the stored document.
    Provider identifiable: MongoDB Atlas (pymongo SDK, MONGODB_ATLAS_URI env var).
    """
    collection = DatabaseClient.get_database()["documents"]
    doc = collection.find_one(
        {"_id": identifier}, read_preference=ReadPreference.PRIMARY
    )
    if not doc:
        raise errors.DocumentNotFound(f"Document with id {identifier} not found")
    # Normalise using helper before returning
    return DatabaseModels.DocumentResponse(**doc).content
