import os
from database_client import NoSQLClient
from database_models import Document

def query_documents(partition_key: str, field: str, value) -> list[dict]:
    """Query documents that match a field/value condition within a partition.

    Uses Amazon DynamoDB's Query API. Assumes the table has a partition key
    named 'pk' and a sort key named 'sk'. The 'field' must be indexable.
    """
    client = NoSQLClient()
    response = client.query(
        TableName=os.getenv('DYNAMODB_TABLE'),
        IndexName='gsi1',               # Global Secondary Index covering field
        KeyConditionExpression=client.Key('pk').eq(partition_key) &
                                 client.Key(field).eq(value)
    )
    items = response.get('Items', [])
    return [Document.from_dict(itm).to_dict() for itm in items]
