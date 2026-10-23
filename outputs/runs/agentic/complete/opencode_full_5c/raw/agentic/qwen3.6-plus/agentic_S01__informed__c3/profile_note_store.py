import os
from pymongo import MongoClient
from identity_models import NoteStoreRequest, NoteStoreResponse


MONGODB_ATLAS_URI = os.environ.get("MONGODB_ATLAS_URI", "mongodb://localhost:27017")
MONGODB_ATLAS_DATABASE = os.environ.get("MONGODB_ATLAS_DATABASE", "onboarding_db")
MONGODB_ATLAS_COLLECTION = os.environ.get(
    "MONGODB_ATLAS_COLLECTION", "onboarding_notes"
)


def persist_onboarding_notes(
    user_id: str,
    notes: dict,
    metadata: dict = None,
    database: str = None,
    collection: str = None,
) -> NoteStoreResponse:
    database = database or MONGODB_ATLAS_DATABASE
    collection = collection or MONGODB_ATLAS_COLLECTION

    request = NoteStoreRequest(
        user_id=user_id,
        notes=notes,
        metadata=metadata or {},
    )

    client = MongoClient(MONGODB_ATLAS_URI)
    db = client[database]
    col = db[collection]

    document = request.to_mongo_document(collection=collection)
    insert_result = col.insert_one(document)

    client.close()

    response = NoteStoreResponse.from_mongo_insert(insert_result)
    response.user_id = user_id
    return response


if __name__ == "__main__":
    result = persist_onboarding_notes(
        user_id="auth0|123456",
        notes={
            "welcome_translated": True,
            "moderation_passed": True,
            "locale": "es",
        },
        metadata={"source": "onboarding_pipeline"},
    )
    print(result)
