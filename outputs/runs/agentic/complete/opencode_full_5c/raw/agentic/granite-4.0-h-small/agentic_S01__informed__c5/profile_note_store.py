# profile_note_store.py - Persist onboarding notes and support metadata in a managed document store
# Using Azure Cosmos DB (NoSQL) as the concrete provider

import os
import json
import uuid
from datetime import datetime
from azure.cosmos import CosmosClient, PartitionKey, CosmosHttpClientError

COSMOS_ENDPOINT = os.getenv("AZURE_COSMOS_ENDPOINT")
COSMOS_KEY = os.getenv("AZURE_COSMOS_KEY")
DATABASE_NAME = "onboarding_db"
CONTAINER_NAME = "notes_container"

client = CosmosClient(COSMOS_ENDPOINT, CosmosClient.from_account_key(COSMOS_KEY))

database = client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)


class NoteDocument:
    def __init__(self, user_id: str, locale: str, notes: List[str], metadata: dict):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.locale = locale
        self.notes = notes  # list of strings
        self.metadata = metadata  # free‑form dict
        self.created_at = datetime.utcnow().isoformat() + "Z"
        self.type = "onboarding_note"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "locale": self.locale,
            "notes": self.notes,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "type": self.type,
        }


def store_note(user_id: str, locale: str, notes: List[str], metadata: dict) -> str:
    """Persist an onboarding note document and return its Azure Cosmos DB id.",

    Normalises the user_id (lower‑case) and handles transient HTTP errors by retrying once.",
    """
    doc = NoteDocument(
        user_id=user_id.lower(), locale=locale, notes=notes, metadata=metadata
    )
    try:
        container.upsert_item(doc.to_dict())
    except CosmosHttpClientError as e:
        if e.status_code in (429, 500, 502):  # throttling / temporary error
            client.reset_client()
            container.upsert_item(doc.to_dict())
        else:
            raise
    return doc.id
