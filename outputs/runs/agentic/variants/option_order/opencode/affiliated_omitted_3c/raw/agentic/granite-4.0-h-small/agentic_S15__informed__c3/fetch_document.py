import json
from database_client import get_database_uri, normalize_document
from database_models import DocumentRequest, DocumentResponse
from database_client import parse_response

# Managed NoSQL Document Store integration (concrete provider)
# Example implementation for Azure Cosmos DB for NoSQL using azure-cosmos SDK
from azure.cosmos import CosmosClient, exceptions

# Initialise client once (assumes AZURE_COSMOS_ENDPOINT and AZURE_COSMOS_KEY are set)
endpoint = get_database_uri()
key = get_env_or_raise("AZURE_COSMOS_KEY")
client = CosmosClient(endpoint, credential=key)

def fetch_document(primary_id: str) -> DocumentResponse:
    """Retrieve a document by its primary identifier from the managed NoSQL store.
    Uses the environment‑identified provider URI; here we target Cosmos DB.
    Args:
        primary_id: Unique identifier for the document.
    Returns:
        DocumentResponse containing the fetched document.
    """
    database_name = get_env_or_raise("COSMOS_DATABASE_NAME")
    container_name = get_env_or_raise("COSMOS_CONTAINER_NAME")
    container = client.get_database_client(database_name).get_container_client(container_name)

    try:
        # Cosmos DB uses the item id field (default name "id")
        response = container.read_item(item=primary_id)
    except exceptions.CosmosResourceNotFoundError:
        raise KeyError(f"Document with id '{primary_id}' not found")
    except exceptions.CosmosHttpResponseError as e:
        raise RuntimeError(f"Cosmos fetch error: {e}")

    # Normalize provider response into our common shape
    raw = response.get('item',{})
    return parse_response(raw)

# Generic helper for missing env variables
get_env_or_raise = lambda var: 
    os.getenv(var) or (lambda: (_ for _ in ()).throw(RuntimeError(f"Missing env {var}")))()()
