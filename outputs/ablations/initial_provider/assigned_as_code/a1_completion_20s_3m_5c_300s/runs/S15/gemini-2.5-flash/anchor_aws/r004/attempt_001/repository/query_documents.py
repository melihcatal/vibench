import boto3
from boto3.dynamodb.conditions import Key, Attr
from database_client import get_dynamodb_table
from database_models import DocumentConfig, DocumentRecord
from typing import List, Dict, Any

def query_documents(field_name: str, field_value: Any, config: DocumentConfig) -> List[DocumentRecord]:
    table = get_dynamodb_table(config)
    response = table.query(
        IndexName=f'{field_name}-index',  # Assuming a GSI for querying
        KeyConditionExpression=Key(field_name).eq(field_value)
    )
    # If no GSI is used, then scan could be used:
    # response = table.scan(
    #    FilterExpression=Attr(field_name).eq(field_value)
    # )
    return [DocumentRecord(id=item[config.key_field], data=item) for item in response.get('Items', [])]
