import os
from typing import List
from identity_models import LoginAuditRecord
from datetime import datetime
from azure.cosmos import CosmosClient, PartitionKey


def persist_audit_records(records: List[LoginAuditRecord]) -> None:
    endpoint = os.getenv("AZURE_COSMOS_ENDPOINT")
    key = os.getenv("AZURE_COSMOS_KEY")
    database_name = "FederatedLoginAudit"
    container_name = "LoginRecords"
    
    client = CosmosClient(endpoint, key)
    database = client.create_database_if_not_exists(id=database_name)
    container = database.create_container_if_not_exists(
        id=container_name,
        partition_key=PartitionKey(path="/provider"),
    )
    
    for record in records:
        container.upsert_item({
            "id": f"{record.user_id}-{record.timestamp}",
            "user_id": record.user_id,
            "provider": record.provider,
            "timestamp": record.timestamp,
            "ip_address": record.ip_address,
            "user_agent": record.user_agent,
            "claims": record.claims,
            "status": record.status,
        })}