from identity_client import get_cosmos_db_client
from identity_models import LoginAuditEvent
import uuid

DATABASE_NAME = "FederatedLoginAudit"
CONTAINER_NAME = "LoginEvents"


def persist_login_audit_event(event: LoginAuditEvent):
    """
    Persists a federated login audit event to Azure Cosmos DB.
    """
    client = get_cosmos_db_client()
    database = client.get_database_client(DATABASE_NAME)
    container = database.get_container_client(CONTAINER_NAME)

    event_dict = event.dict()
    event_dict["id"] = str(uuid.uuid4())

    container.create_item(body=event_dict)
    return event_dict["id"]


# Example Usage would require setting up the DB and container in Azure.
# db = client.create_database_if_not_exists(id=DATABASE_NAME)
# container = db.create_container_if_not_exists(id=CONTAINER_NAME, partition_key=PartitionKey(path="/user_id"))
