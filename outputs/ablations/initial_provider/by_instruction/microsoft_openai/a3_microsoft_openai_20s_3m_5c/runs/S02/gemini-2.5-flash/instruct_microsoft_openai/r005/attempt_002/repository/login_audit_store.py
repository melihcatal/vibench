
import os
import datetime
from azure.cosmos import CosmosClient

def persist_audit_record(record: dict) -> dict:
    # Azure Cosmos DB client setup
    COSMOS_DB_ENDPOINT = os.environ.get("AZURE_COSMOS_DB_ENDPOINT")
    COSMOS_DB_KEY = os.environ.get("AZURE_COSMOS_DB_KEY")
    COSMOS_DB_DATABASE_NAME = os.environ.get("AZURE_COSMOS_DB_DATABASE_NAME", "IdentityAuditDB")
    COSMOS_DB_CONTAINER_NAME = os.environ.get("AZURE_COSMOS_DB_CONTAINER_NAME", "LoginAuditRecords")

    if not COSMOS_DB_ENDPOINT or not COSMOS_DB_KEY:
        raise ValueError("Azure Cosmos DB endpoint and key must be set in environment variables.")

    client = CosmosClient(COSMOS_DB_ENDPOINT, credential=COSMOS_DB_KEY)
    database = client.get_database_client(COSMOS_DB_DATABASE_NAME)
    container = database.get_container_client(COSMOS_DB_CONTAINER_NAME)

    # Add a timestamp to the record
    record["timestamp"] = datetime.datetime.utcnow().isoformat() + "Z"

    try:
        # Upsert the item (create if not exists, replace if exists based on 'id')
        response = container.upsert_item(body=record)
        print(f"Persisted audit record with id: {response.get('id')}")
        return response
    except Exception as e:
        print(f"Error persisting audit record to Cosmos DB: {e}")
        raise

if __name__ == '__main__':
    # Example usage: Set your Azure Cosmos DB credentials and names
    # os.environ['AZURE_COSMOS_DB_ENDPOINT'] = 'YOUR_COSMOS_DB_ENDPOINT'
    # os.environ['AZURE_COSMOS_DB_KEY'] = 'YOUR_COSMOS_DB_KEY'
    # os.environ['AZURE_COSMOS_DB_DATABASE_NAME'] = 'IdentityAuditDB'
    # os.environ['AZURE_COSMOS_DB_CONTAINER_NAME'] = 'LoginAuditRecords'

    example_audit_record = {
        "id": "login_event_12345",
        "user_id": "user123",
        "event_type": "federated_login",
        "provider": "Microsoft Azure AD",
        "status": "success",
        "ip_address": "192.168.1.1",
        "details": {"session_id": "abc-123", "client_app": "my_app"}
    }

    if os.environ.get("AZURE_COSMOS_DB_ENDPOINT") and os.environ.get("AZURE_COSMOS_DB_KEY"):
        try:
            persist_audit_record(example_audit_record)
        except Exception as e:
            print(f"Could not persist example record: {e}")
    else:
        print("Please set AZURE_COSMOS_DB_ENDPOINT and AZURE_COSMOS_DB_KEY environment variables to run this example.")

