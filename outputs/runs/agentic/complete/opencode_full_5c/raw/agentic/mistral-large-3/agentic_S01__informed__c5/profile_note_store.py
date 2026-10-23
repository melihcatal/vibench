import os
import uuid
from typing import Dict, Any
from azure.cosmos import CosmosClient, PartitionKey
from pydantic import BaseModel


class ProfileNoteRequest(BaseModel):
    user_id: str
    notes: Dict[str, Any]
    metadata: Dict[str, Any]


class ProfileNoteResponse(BaseModel):
    id: str
    user_id: str
    status: str


class CosmosDBClient:
    def __init__(self):
        self.endpoint = os.getenv("AZURE_COSMOS_ENDPOINT")
        self.key = os.getenv("AZURE_COSMOS_KEY")
        self.database_name = "OnboardingDB"
        self.container_name = "ProfileNotes"
        self.client = CosmosClient(self.endpoint, self.key)
        self.database = self.client.create_database_if_not_exists(id=self.database_name)
        self.container = self.database.create_container_if_not_exists(
            id=self.container_name,
            partition_key=PartitionKey(path="/user_id"),
        )

    def store_profile_note(self, request: ProfileNoteRequest) -> ProfileNoteResponse:
        document = {
            "id": str(uuid.uuid4()),
            "user_id": request.user_id,
            "notes": request.notes,
            "metadata": request.metadata,
        }
        self.container.create_item(body=document)
        return ProfileNoteResponse(
            id=document["id"],
            user_id=request.user_id,
            status="stored",
        )


def profile_note_store(
    user_id: str, notes: Dict[str, Any], metadata: Dict[str, Any]
) -> ProfileNoteResponse:
    client = CosmosDBClient()
    request = ProfileNoteRequest(user_id=user_id, notes=notes, metadata=metadata)
    return client.store_profile_note(request)
