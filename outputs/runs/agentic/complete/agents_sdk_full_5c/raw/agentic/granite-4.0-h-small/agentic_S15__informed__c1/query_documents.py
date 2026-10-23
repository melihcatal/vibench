import os
from database_client import get_dynamodb_client
from database_models import Document

# Managed NoSQL store: Amazon DynamoDB (with secondary index for queries)

def query_documents(partition_key: str, value: str, index_name: str = 'gbk-index') -> list[Document]:
    """Query documents that share a given partition/key field value.

    Uses a global secondary index named 'gbk-index' by default.
    Returns a list of Document objects.
    """
    client = get_dynamodb_client()
    response = client.query(
        TableName=os.getenv('DYNAMODB_TABLE'),
        IndexName=index_name,
        KeyConditionExpression={
            'ExpressionAttributeNames': {'#gbk': partition_key},
            'ExpressionAttributeValues': {':val': {'S': value}},
            'Expression': '#gbk = :val'
        }
    )
    items = response.get('Items', [])
    return [Document.from_dynamodb_item(it) for it in items]

if __name__ == "__main__":
    # Example query: find all docs with tag 'python'
    docs = query_documents('tags', 'python')
    print('Queried docs count:', len(docs))
