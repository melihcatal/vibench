from typing import Dict, Any, List
import boto3
from boto3.dynamodb.conditions import Key
from database_client import get_dynamodb_table

def query_documents(field_name: str, field_value: Any) -> List[Dict[str, Any]]:
    table = get_dynamodb_table()
    response = table.query(
        IndexName=f"{field_name}-index",
        KeyConditionExpression=Key(field_name).eq(field_value)
    )
    return response.get("Items", [])