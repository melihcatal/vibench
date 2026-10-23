import json
from database_client import NoSQLClient

def fetch_document(identifier):
    """Fetch a document by its primary identifier from the managed NoSQL store.

    Uses Azure Cosmos DB for NoSQL.
    """
    client = NoSQLClient()
    container = client.get_container('my_database', 'my_container')
    # Assuming documents have an 'id' field that matches the identifier
    item = container.read_item(item={'id': identifier}, partition_key='default')
    return item
