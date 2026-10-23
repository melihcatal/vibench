import uuid
from datetime import datetime
import os
import json

# Managed document store client (Azure Cosmos DB DocumentClient wrapper example)

class DocumentClient:
    def __init__(self, endpoint, key):
        # Using Azure Cosmos DB SDK for illustration
        import azure.cosmos as cosmos
        self.client = cosmos.CosmosClient(endpoint, {'masterKey': key})
        self.database_name = "FederatedLogDB"
        self.container_name = "LoginAudit"
        # Create DB and container if missing (demo only)
        try:
            self.client.create_database(self.database_name)
        except Exception:
            pass
        db = self.client.get_database_client(self.database_name)
        try:
            db.create_container(id=self.container_name, partition_key=cosmos.PartitionKey(path="/user_id"))
        except Exception:
            pass
        self.container = db.get_container_client(self.container_name)
    
    def upsert_audit(self, record: dict):
        # Use a generated ID to avoid duplicates
        record_id = str(uuid.uuid4())
        # Ensure required fields exist
        record["id"] = record_id
        record["timestamp"] = datetime.utcnow().isoformat()
        # Upsert (replace if exists with same id)
        self.container.upsert_item(record)

# Global singleton (for demo; in production instantiate per service)
audit_store = DocumentClient(
    endpoint=os.getenv("COSMOS_ENDPOINT"),
    key=os.getenv("COSMOS_KEY")
)

# Public API for persisting a login audit event

def record_login_audit(user_id: str, auth_method: str):
    payload = {
        "user_id": user_id,
        "event": "login",
        "auth_method": auth_method,
        "additional_info": {}
    }
    audit_store.upsert_audit(payload)

# Example query to retrieve all login events for a user

def get_user_logins(user_id: str):
    # Cosmos SQL query string
    query = f"SELECT * FROM c WHERE c.user_id = '{user_id}' AND c.event = 'login'"
    items = list(audit_store.container.query_items(query=query, enable_cross_partition_query=True))
    return items

# Example: summarize latest 10 logins for a user

def latest_logins_summary(user_id: str, limit: int = 10):
    logs = get_user_logins(user_id)
    return logs[:limit]

if __name__ == "__main__":
    # Demo placeholder
    pass
