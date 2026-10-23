from database_client import get_dynamodb_table
from database_models import Document, document_from_item
from botocore.exceptions import ClientError

def fetch_document(document_id: str) -> Document | None:
    table = get_dynamodb_table()
    try:
        response = table.get_item(Key={'id': document_id})
        item = response.get('Item')
        if item:
            return document_from_item(item)
        return None
    except ClientError as e:
        raise e
