from azure.cosmos import CosmosClient, PartitionKey
import os
from typing import Dict, Any, List
from datetime import datetime

# Azure Cosmos DB Configuration
COSMOS_DB_ENDPOINT = os.getenv(
    "COSMOS_DB_ENDPOINT", "https://your-account.documents.azure.com:443/"
)
COSMOS_DB_KEY = os.getenv("COSMOS_DB_KEY", "your-cosmos-db-key")
COSMOS_DB_DATABASE = os.getenv("COSMOS_DB_DATABASE", "FederatedLoginAudit")
COSMOS_DB_CONTAINER = os.getenv("COSMOS_DB_CONTAINER", "AuditEvents")


class LoginAuditStore:
    def __init__(self):
        self.client = CosmosClient(COSMOS_DB_ENDPOINT, credential=COSMOS_DB_KEY)
        self.database = self.client.get_database_client(COSMOS_DB_DATABASE)
        self.container = self.database.get_container_client(COSMOS_DB_CONTAINER)

    def persist_audit_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Persist federated login audit event to Azure Cosmos DB."""
        event["id"] = f"{event['user_id']}-{event['timestamp']}"
        event["partitionKey"] = event["provider"]
        return self.container.create_item(body=event)

    def fetch_audit_events(
        self, user_id: str, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Fetch federated login audit events for a user from Azure Cosmos DB."""
        query = "SELECT * FROM c WHERE c.user_id = @user_id ORDER BY c.timestamp DESC"
        parameters = [{"name": "@user_id", "value": user_id}]
        items = list(
            self.container.query_items(
                query=query,
                parameters=parameters,
                enable_cross_partition_query=True,
                max_item_count=limit,
            )
        )
        return items
