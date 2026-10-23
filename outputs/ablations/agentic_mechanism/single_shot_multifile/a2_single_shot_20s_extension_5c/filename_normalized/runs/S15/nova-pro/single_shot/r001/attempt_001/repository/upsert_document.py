from database_client import get_db_client

def upsert_document(document_id, document):
    client = get_db_client()
    client.put_item(TableName='ManagedNoSQLTable', Item={'id': {'S': document_id}, 'document': {'S': json.dumps(document)}})