import os
import json
from azure.identity import DefaultAzureCredential
from azure.cosmos import CosmosClient

# Configuration keys expected in the environment
COSMOS_URI = os.getenv('AZURE_COSMOS_URI')
COSMOS_KEY = os.getenv('AZURE_COSMOS_KEY')
DATABASE_NAME = os.getenv('AZURE_COSMOS_DATABASE')
CONTAINER_NAME = os.getenv('AZURE_COSMOS_CONTAINER')

if not all([COSMOS_URI, COSMOS_KEY, DATABASE_NAME, CONTAINER_NAME]):
    raise RuntimeError('Missing Cosmos DB configuration in environment variables')

credential = DefaultAzureCredential()
client = CosmosClient(COSMOS_URI, credential=credential)

def get_or_create_database():
    return client.get_database_client(DATABASE_NAME)

def get_or_create_container():
    db = get_or_create_database()
    return db.get_container_client(CONTAINER_NAME)

def store_login_event(event):
    """Persist a normalized login event JSON document to Azure Cosmos DB."""
    container = get_or_create_container()
    # Use a GUID or a timestamp as the item ID for simplicity
    from uuid import uuid4
    item_id = str(uuid4())
    container.upsert_item({'id': item_id, **event})
    return item_id

def load_login_events(limit=20):
    """Retrieve the most recent login events from Cosmos DB."""
    container = get_or_create_container()
    # Run a simple query ordered by a hypothetical timestamp field
    query = container.query_items(
        query="SELECT * FROM c ORDER BY c.timestamp DESC",
        parameters=[],
        max_item_count=limit,
    )
    return list(query)

# Example usage – store a demo event
if __name__ == '__main__':
    sample_event = {
        'user_id': 'user-12345',
        'source': 'Microsoft Entra ID',
        'timestamp': '2025-08-15T12:34:56Z',
        'claims': {'sub': 'user-12345', 'name': 'Jane Doe'}
    }
    event_id = store_login_event(sample_event)
    print(f'Stored event ID: {event_id}')

    events = load_login_events(limit=5)
    print('Recent events:')
    for ev in events:
        print(json.dumps(ev, indent=2))
