import json
from database_client import get_dynamodb_client, get_dynamodb_table_name
from database_models import Document

def fetch_document(document_id: str) -> Document | None:
    dynamodb = get_dynamodb_client()
    table_name = get_dynamodb_table_name()

    response = dynamodb.get_item(
        TableName=table_name,
        Key={
            'id': {'S': document_id}
        }
    )

    item = response.get('Item')
    if not item:
        return None

    return Document(
        id=item['id']['S'],
        content=json.loads(item['content']['S'])
    )
