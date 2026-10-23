from database_client import get_dynamodb_resource
from database_models import Document
from typing import Optional

def fetch_document(table_name: str, document_id: str) -> Optional[Document]:
    """
    Fetches a document by identifier from a managed NoSQL store (DynamoDB).
    """
    dynamodb = get_dynamodb_resource()
    table = dynamodb.Table(table_name)

    response = table.get_item(
        Key={
            'id': document_id
        }
    )
    item = response.get('Item')

    if item:
        return Document(**item)
    return None
