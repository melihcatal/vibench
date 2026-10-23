import json
from database_client import NoSQLClient

def conditional_update(identifier, new_fields, condition_expression, condition_values=None):
    """Perform a conditional or version-aware update of a document.

    Demonstrates Azure Cosmos DB's optimistic concurrency using ETag.
    """
    client = NoSQLClient()
    container = client.get_container('my_database', 'my_container')
    # Retrieve current ETag for concurrency check
    current_item = container.read_item(item={'id': identifier}, partition_key='default')
    etag = current_item['_etag']
    # Build the update payload with ETag condition
    update_item = {
        'id': identifier,
        **new_fields,
    }
    # Azure SDK conditional update pattern
    container.replace_item(item=update_item, partition_key='default', item['etag']=etag)
