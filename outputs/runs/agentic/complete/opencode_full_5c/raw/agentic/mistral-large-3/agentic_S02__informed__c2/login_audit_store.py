from typing import Dict, Any
from datetime import datetime
from azure.cosmos import CosmosClient, PartitionKey
import os


class LoginAuditStore:
    """
    Persist federated-login audit records in Azure Cosmos DB.
    """

    def __init__(self):
        self.endpoint = os.getenv("AZURE_COSMOS_ENDPOINT")
        self.key = os.getenv("AZURE_COSMOS_KEY")
        self.client = CosmosClient(self.endpoint, self.key)
        self.database_name = "FederatedLoginAudit"
        self.container_name = "AuditRecords"
        self._initialize_db()

    def _initialize_db(self):
        """Initialize database and container if they don't exist."""
        try:
            self.database = self.client.create_database_if_not_exists(
                id=self.database_name
            )
            self.container = self.database.create_container_if_not_exists(
                id=self.container_name, partition_key=PartitionKey(path="/userId")
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Cosmos DB: {e}")

    def persist_audit_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Persist a federated-login audit record.
        Returns the persisted record with metadata.
        """
        record["id"] = str(
            record.get("id", record["userId"] + "_" + datetime.utcnow().isoformat())
        )
        record["timestamp"] = datetime.utcnow().isoformat()

        persisted_record = self.container.create_item(body=record)
        return persisted_record
