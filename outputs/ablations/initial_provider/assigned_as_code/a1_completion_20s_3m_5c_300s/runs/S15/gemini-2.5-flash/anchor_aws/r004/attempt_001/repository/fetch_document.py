import boto3
from boto3.dynamodb.conditions import Key
from database_client import get_dynamodb_table
from database_models import DocumentConfig, DocumentRecord

def fetch_document(document_id: str, config: DocumentConfig) -> DocumentRecord | None:
    table = get_dynamodb_table(config)
    response = table.get_item(Key={config.key_field: document_id})
    item = response.get('Item')
    if item:
        return DocumentRecord(id=item[config.key_field], data=item)
    return None
