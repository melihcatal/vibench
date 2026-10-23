from database_client import get_db_client

def conditional_update(document_id, document, expected_version):
    client = get_db_client()
    client.update_item(
        TableName='ManagedNoSQLTable',
        Key={'id': {'S': document_id}},
        UpdateExpression='SET document = :document',
        ConditionExpression='attribute_exists(id) AND document.version = :version',
        ExpressionAttributeValues={
            ':document': {'S': json.dumps(document)},
            ':version': {'N': str(expected_version)}
        }
    )