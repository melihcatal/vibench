import os
import uuid
from datetime import datetime
from azure.cosmos import CosmosClient, PartitionKey
from identity_models import ProfileNote


def store_profile_note(
    user_id: str, content: str, note_type: str = "support", metadata: dict = None
) -> ProfileNote:
    """
    Persist onboarding notes and support metadata in Azure Cosmos DB.
    """
    endpoint = os.getenv("AZURE_COSMOS_ENDPOINT", "")
    key = os.getenv("AZURE_COSMOS_KEY", "")
    database_name = os.getenv("AZURE_COSMOS_DATABASE", "onboarding")
    container_name = os.getenv("AZURE_COSMOS_CONTAINER", "profile_notes")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_COSMOS_ENDPOINT and AZURE_COSMOS_KEY environment variables are required"
        )

    # Initialize Cosmos DB client
    client = CosmosClient(endpoint, key)

    # Get or create database and container
    database = client.create_database_if_not_exists(id=database_name)
    container = database.create_container_if_not_exists(
        id=container_name, partition_key=PartitionKey(path="/user_id")
    )

    # Create note document
    note_id = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat() + "Z"

    note_document = {
        "id": note_id,
        "user_id": user_id,
        "content": content,
        "note_type": note_type,
        "created_at": created_at,
        "metadata": metadata or {},
    }

    # Store in Cosmos DB
    container.create_item(body=note_document)

    return ProfileNote(
        user_id=user_id,
        note_id=note_id,
        content=content,
        note_type=note_type,
        created_at=created_at,
        metadata=note_document["metadata"],
    )


def get_profile_notes(user_id: str, limit: int = 10) -> list:
    """
    Retrieve profile notes for a user from Azure Cosmos DB.
    """
    endpoint = os.getenv("AZURE_COSMOS_ENDPOINT", "")
    key = os.getenv("AZURE_COSMOS_KEY", "")
    database_name = os.getenv("AZURE_COSMOS_DATABASE", "onboarding")
    container_name = os.getenv("AZURE_COSMOS_CONTAINER", "profile_notes")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_COSMOS_ENDPOINT and AZURE_COSMOS_KEY environment variables are required"
        )

    # Initialize Cosmos DB client
    client = CosmosClient(endpoint, key)

    # Get database and container
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)

    # Query notes for user
    query = f"SELECT * FROM c WHERE c.user_id = @user_id ORDER BY c.created_at DESC OFFSET 0 LIMIT @limit"
    parameters = [
        {"name": "@user_id", "value": user_id},
        {"name": "@limit", "value": limit},
    ]

    notes = []
    for item in container.query_items(
        query=query, parameters=parameters, enable_cross_partition_query=False
    ):
        notes.append(
            ProfileNote(
                user_id=item["user_id"],
                note_id=item["id"],
                content=item["content"],
                note_type=item["note_type"],
                created_at=item["created_at"],
                metadata=item.get("metadata", {}),
            )
        )

    return notes
