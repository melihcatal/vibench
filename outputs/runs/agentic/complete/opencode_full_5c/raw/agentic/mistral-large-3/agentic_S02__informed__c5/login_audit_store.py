# Federated Login Flow - Login Audit Store

import os
from typing import Dict, List
from identity_models import AuditEvent
from azure.cosmos import CosmosClient, PartitionKey


def login_audit_store(events: List[AuditEvent]) -> bool:
    """Persist federated-login audit records in Azure Cosmos DB."""
    endpoint = os.getenv("AZURE_COSMOS_ENDPOINT")
    key = os.getenv("AZURE_COSMOS_KEY")
    database_name = "FederatedLoginAudit"
    container_name = "AuditEvents"

    client = CosmosClient(endpoint, key)
    database = client.create_database_if_not_exists(id=database_name)
    container = database.create_container_if_not_exists(
        id=container_name, partition_key=PartitionKey(path="/user_id")
    )

    for event in events:
        container.upsert_item(
            {
                "id": event.event_id,
                "timestamp": event.timestamp,
                "user_id": event.user_id,
                "provider": event.provider,
                "action": event.action,
                "metadata": event.metadata,
                "ip_address": event.ip_address,
                "user_agent": event.user_agent,
            }
        )

    return True
