from __future__ import annotations

from typing import Any, Dict

from azure.cosmos import CosmosClient

AZURE_COSMOS_ENDPOINT = ""
AZURE_COSMOS_KEY = ""
COSMOS_DATABASE = "federated-login"
COSMOS_CONTAINER = "audit-records"


def persist_audit_record(record: Dict[str, Any]) -> Dict[str, Any]:
    client = CosmosClient(AZURE_COSMOS_ENDPOINT, credential=AZURE_COSMOS_KEY)
    database = client.create_database_if_not_exists(id=COSMOS_DATABASE)
    container = database.create_container_if_not_exists(id=COSMOS_CONTAINER, partition_key="/subject")
    container.upsert_item(record)
    return record
