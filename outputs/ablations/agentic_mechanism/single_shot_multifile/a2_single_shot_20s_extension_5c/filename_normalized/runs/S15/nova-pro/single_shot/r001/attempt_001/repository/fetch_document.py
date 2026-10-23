from database_client import get_db_client

def fetch_document(document_id):
    client = get_db_client()
    response = client.get_item(TableName='ManagedNoSQLTable', Key={'id': {'S': document_id}})
    item = response.get('Item', {})
    return json.loads(item.get('document', {}).get('S', '{}'))