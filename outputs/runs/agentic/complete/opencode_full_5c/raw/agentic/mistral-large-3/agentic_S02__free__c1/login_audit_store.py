from azure.cosmos import CosmosClient, PartitionKey
import os
from typing import Dict, Any
from identity_models import FederatedLoginEvent


# Azure Cosmos DB for audit storage
def get_cosmos_client():
    endpoint = os.getenv("COSMOS_ENDPOINT")
    key = os.getenv("COSMOS_KEY")
    client = CosmosClient(endpoint, key)
    return client


def persist_login_audit(event: FederatedLoginEvent) -> str:
    client = get_cosmos_client()
    database_name = "FederatedLoginAudit"
    container_name = "LoginEvents"

    database = client.create_database_if_not_exists(id=database_name)
    container = database.create_container_if_not_exists(
        id=container_name, partition_key=PartitionKey(path="/provider")
    )

    item = {
        "id": event.event_id,
        "user_id": event.user_id,
        "provider": event.provider,
        "timestamp": event.timestamp,
        "claims": {
            "sub": event.claims.sub,
            "name": event.claims.name,
            "email": event.claims.email,
            "email_verified": event.claims.email_verified,
        },
        "ip_address": event.ip_address,
        "user_agent": event.user_agent,
        "metadata": event.metadata,
    }

    container.create_item(body=item)
    return event.event_id
