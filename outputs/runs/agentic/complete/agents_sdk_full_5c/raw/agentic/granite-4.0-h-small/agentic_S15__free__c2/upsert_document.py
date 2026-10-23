import json
from database_client import NoSQLClient

def upsert_document(identifier, document):
    """Upsert a JSON document into the managed NoSQL store.

    Uses Azure Cosmos DB for NoSQL.
    """
    client = NoSQLClient()
    container = client.get_container('my_database', 'my_container')
    # Use merge_upsert to insert or replace
    container.upsert_item({'id': identifier, **document})
