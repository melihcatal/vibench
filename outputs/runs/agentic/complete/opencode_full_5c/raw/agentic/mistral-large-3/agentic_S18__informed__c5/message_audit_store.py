from azure.cosmos import CosmosClient, PartitionKey
import os
from typing import Dict, Any, Optional

endpoint = os.getenv("AZURE_COSMOS_ENDPOINT")
key = os.getenv("AZURE_COSMOS_KEY")
client = CosmosClient(endpoint, key)

database_name = "MessageAuditDB"
container_name = "ProcessedMessages"

database = client.create_database_if_not_exists(id=database_name)
container = database.create_container_if_not_exists(
    id=container_name, partition_key=PartitionKey(path="/event_id")
)


def message_audit_store(message: Dict[str, Any]) -> str:
    response = container.create_item(body=message)
    return response["id"]
