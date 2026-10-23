# [SAME-SCENARIO] fetch_document.py
from database_client import NoSQLClient

def fetch_document(doc_id):
    """Fetch a document by its primary identifier from the managed NoSQL store.

    Args:
        doc_id (str): The document's primary key.
    Returns:
        dict: The deserialized document payload.
    """
    client = NoSQLClient()
    response = client.get_item(TableName=client.table_name, Key={'id': {'S': doc_id}})
    item = response.get('Item', {})
    return json.loads(item.get('content', '{}'))