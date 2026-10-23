import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.exceptions import CosmosHttpResponseError

_cosmos_client = None
_database = None
_container = None


def get_cosmos_client():
    """Get or initialize Azure Cosmos DB client."""
    global _cosmos_client, _database, _container

    if _cosmos_client is None:
        endpoint = os.getenv("AZURE_COSMOS_ENDPOINT")
        key = os.getenv("AZURE_COSMOS_KEY")

        if not endpoint or not key:
            raise RuntimeError(
                "Azure Cosmos DB credentials not found. "
                "Set AZURE_COSMOS_ENDPOINT and AZURE_COSMOS_KEY environment variables."
            )

        _cosmos_client = CosmosClient(endpoint, key)

        # Get or create database
        database_name = "onboarding_db"
        try:
            _database = _cosmos_client.get_database_client(database_name)
            _database.read()
        except CosmosHttpResponseError:
            _database = _cosmos_client.create_database(database_name)

        # Get or create container
        container_name = "profile_notes"
        try:
            _container = _database.get_container_client(container_name)
            _container.read()
        except CosmosHttpResponseError:
            _container = _database.create_container(
                id=container_name,
                partition_key=PartitionKey(path="/user_id"),
                default_ttl=7776000,  # 90 days in seconds
            )

    return _container


def store_onboarding_note(
    user_id: str,
    note_type: str,
    content: Dict[str, Any],
    metadata: Dict[str, Any] = None,
) -> Dict[str, Any]:
    """Persist onboarding notes and support metadata in Azure Cosmos DB."""
    container = get_cosmos_client()

    note_id = f"{user_id}_{note_type}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

    document = {
        "id": note_id,
        "user_id": user_id,
        "note_type": note_type,
        "content": content,
        "metadata": metadata or {},
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
        "provider": "azure_cosmos_db",
        "ttl": 7776000,  # 90 days
    }

    try:
        response = container.create_item(body=document)
        return {
            "note_id": note_id,
            "user_id": user_id,
            "note_type": note_type,
            "created": True,
            "etag": response.get("_etag"),
            "timestamp": response.get("_ts"),
            "provider": "azure_cosmos_db",
        }
    except CosmosHttpResponseError as e:
        raise RuntimeError(f"Failed to store note in Cosmos DB: {str(e)}")


def get_user_notes(
    user_id: str, note_type: Optional[str] = None, limit: int = 100
) -> List[Dict[str, Any]]:
    """Retrieve onboarding notes for a specific user."""
    container = get_cosmos_client()

    query = "SELECT * FROM c WHERE c.user_id = @user_id"
    parameters = [{"name": "@user_id", "value": user_id}]

    if note_type:
        query += " AND c.note_type = @note_type"
        parameters.append({"name": "@note_type", "value": note_type})

    query += " ORDER BY c.created_at DESC"

    try:
        items = list(
            container.query_items(
                query=query, parameters=parameters, max_item_count=limit
            )
        )

        # Remove Cosmos DB internal fields
        for item in items:
            item.pop("_rid", None)
            item.pop("_self", None)
            item.pop("_etag", None)
            item.pop("_attachments", None)
            item.pop("_ts", None)

        return items
    except CosmosHttpResponseError as e:
        raise RuntimeError(f"Failed to retrieve notes from Cosmos DB: {str(e)}")


def update_note(note_id: str, user_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
    """Update an existing onboarding note."""
    container = get_cosmos_client()

    try:
        # First get the existing document
        document = container.read_item(item=note_id, partition_key=user_id)

        # Update fields
        for key, value in updates.items():
            if key not in ["id", "user_id", "created_at", "provider"]:
                document[key] = value

        document["updated_at"] = datetime.utcnow().isoformat()

        # Replace the document
        response = container.replace_item(item=note_id, body=document)

        return {
            "note_id": note_id,
            "user_id": user_id,
            "updated": True,
            "etag": response.get("_etag"),
            "timestamp": response.get("_ts"),
            "provider": "azure_cosmos_db",
        }
    except CosmosHttpResponseError as e:
        if e.status_code == 404:
            raise ValueError(f"Note {note_id} not found for user {user_id}")
        raise RuntimeError(f"Failed to update note in Cosmos DB: {str(e)}")


def delete_note(note_id: str, user_id: str) -> Dict[str, Any]:
    """Delete an onboarding note."""
    container = get_cosmos_client()

    try:
        container.delete_item(item=note_id, partition_key=user_id)
        return {
            "note_id": note_id,
            "user_id": user_id,
            "deleted": True,
            "provider": "azure_cosmos_db",
        }
    except CosmosHttpResponseError as e:
        if e.status_code == 404:
            raise ValueError(f"Note {note_id} not found for user {user_id}")
        raise RuntimeError(f"Failed to delete note from Cosmos DB: {str(e)}")


def store_support_metadata(
    user_id: str, support_data: Dict[str, Any]
) -> Dict[str, Any]:
    """Store support-related metadata for a user."""
    return store_onboarding_note(
        user_id=user_id,
        note_type="support_metadata",
        content=support_data,
        metadata={
            "source": "support_system",
            "priority": support_data.get("priority", "medium"),
            "category": support_data.get("category", "general"),
        },
    )


def store_moderation_result(
    user_id: str, moderation_result: Dict[str, Any]
) -> Dict[str, Any]:
    """Store content moderation results."""
    return store_onboarding_note(
        user_id=user_id,
        note_type="moderation_result",
        content=moderation_result,
        metadata={
            "source": "azure_content_safety",
            "safe": moderation_result.get("safe", False),
            "block_recommended": moderation_result.get("block_recommended", False),
        },
    )


def store_translation_result(
    user_id: str, translation_result: Dict[str, Any]
) -> Dict[str, Any]:
    """Store translation results."""
    return store_onboarding_note(
        user_id=user_id,
        note_type="translation_result",
        content=translation_result,
        metadata={
            "source": "azure_translator",
            "target_language": translation_result.get("target_language"),
            "detected_language": translation_result.get("detected_language"),
        },
    )
