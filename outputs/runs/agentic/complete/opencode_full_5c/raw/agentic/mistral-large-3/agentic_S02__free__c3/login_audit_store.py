import os
from datetime import datetime
from typing import Dict, Any
from identity_models import AuditEvent
from azure.cosmos import CosmosClient, PartitionKey

# Using Azure Cosmos DB for audit record storage
COSMOS_ENDPOINT = os.getenv(
    "COSMOS_ENDPOINT", "https://your-cosmos-account.documents.azure.com:443/"
)
COSMOS_KEY = os.getenv("COSMOS_KEY", "your-cosmos-key")
COSMOS_DATABASE = os.getenv("COSMOS_DATABASE", "FederatedLoginAudit")
COSMOS_CONTAINER = os.getenv("COSMOS_CONTAINER", "AuditEvents")


def persist_audit_event(event: AuditEvent) -> Dict[str, Any]:
    """Persists a federated-login audit event in Azure Cosmos DB."""
    client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
    database = client.get_database_client(COSMOS_DATABASE)
    container = database.get_container_client(COSMOS_CONTAINER)

    event_dict = {
        "id": event.event_id,
        "user_id": event.user_id,
        "event_type": event.event_type,
        "timestamp": event.timestamp,
        "metadata": event.metadata,
    }

    response = container.create_item(event_dict)
    return {
        "id": response["id"],
        "status": "persisted",
        "timestamp": datetime.utcnow().isoformat(),
    }
