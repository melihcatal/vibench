from pydantic import BaseModel, Field

class StoreRequest(BaseModel):
    user_id: str = Field(..., description="Cognito user identifier")
    note_text: str = Field(..., description="Onboarding note from user or support")
    metadata: dict = Field(default_factory=dict, description="Additional metadata (e.g., timestamps)")

class StoreResponse(BaseModel):
    note_id: str = Field(..., description="ID assigned by the document store")

def profile_note_store(req: StoreRequest) -> str:
    """Persists onboarding notes and support metadata in a managed document store.

    Uses AWS DocumentDB (via the MongoDB driver) as the concrete provider.
    Returns the generated note document ID.
    """
    from pymongo import MongoClient

    # Replace with real endpoint, credentials, and database name
    MONGO_URI = "mongodb+srv://your-cluster.mongodb.net/onboarding_notes?retryWrites=true&w=majority"
    db_name = "notes_db"
    collection_name = "user_notes"

    client = MongoClient(MONGO_URI)
    collection = client[db_name][collection_name]

    # Insert one document per onboarding note
    result = collection.insert_one({
        "user_id": req.user_id,
        "note_text": req.note_text,
        **req.metadata
    })
    return str(result.inserted_id)