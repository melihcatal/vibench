from database_client import get_db_client

def query_documents(field_name, field_value):
    client = get_db_client()
    response = client.query(
        TableName='ManagedNoSQLTable',
        KeyConditionExpression='field_name = :value',
        ExpressionAttributeValues={':value': {'S': field_value}}
    )
    return [json.loads(item.get('document', {}).get('S', '{}')) for item in response.get('Items', [])]