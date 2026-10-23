import os
from datetime import datetime
from typing import Optional
from azure.cosmos import CosmosClient, PartitionKey
from identity_models import LoginAuditRecord


class LoginAuditStore:
    def __init__(self, connection_string: Optional[str] = None):
        connection_string = connection_string or os.getenv("COSMOS_DB_CONNECTION_STRING")
        self.client = CosmosClient.from_connection_string(connection_string)
        self.database = self.client.get_database_client("FederatedLoginDB")
        self.container = self.database.get_container_client("AuditRecords")

    def persist_audit_record(self, record: LoginAuditRecord) -> None:
        self.container.upsert_item({
            "id": f"{record.user_id}-{record.timestamp}",
            "user_id": record.user_id,
            "provider": record.provider,
            "timestamp": record.timestamp,
            "ip_address": record.ip_address,
            "user_agent": record.user_agent,
            "claims": record.claims,
        })

    def get_audit_records(self, user_id: str) -> list[dict]:
        query = "SELECT * FROM c WHERE c.user_id = @user_id"
        items = list(self.container.query_items(
            query=query,
            parameters=[{"name": "@user_id", "value": user_id}],
            enable_cross_partition_query=True,
        ))
        return items