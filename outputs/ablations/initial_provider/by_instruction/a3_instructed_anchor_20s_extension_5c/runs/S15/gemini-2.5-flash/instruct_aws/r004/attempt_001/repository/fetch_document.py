from database_client import get_dynamodb_client
from database_models import Document

def fetch_document(table_name: str, document_id: str) -> Document | None:
    dynamodb = get_dynamodb_client()
    response = dynamodb.get_item(
        TableName=table_name,
        Key={
            'id': {'S': document_id}
        }
    )
    item = response.get('Item')
    if item:
        # Convert DynamoDB item format to a regular dictionary
        deserialized_item = {k: list(v.values())[0] for k, v in item.items()}
        return Document.from_item(deserialized_item)
    return None
