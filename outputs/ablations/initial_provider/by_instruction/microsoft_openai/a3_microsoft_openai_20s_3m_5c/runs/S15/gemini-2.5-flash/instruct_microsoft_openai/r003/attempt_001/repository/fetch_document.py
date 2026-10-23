from database_client import CosmosDBClient
from database_models import Document

def fetch_document(document_id: str, partition_key: str):
    client = CosmosDBClient()
    container = client.get_container()
    # In Cosmos DB, 'id' is a logical partition key when not specified otherwise
    # Assuming document_id can also act as partition_key for simplicity if no explicit partition key is given
    # For robust applications, actual partition key path should be known.
    response = container.read_item(item=document_id, partition_key=partition_key)
    return Document.from_dict(response)
