import os
from typing import List, Any
from database_client import get_dynamodb_client, get_table_name, serialize_item, deserialize_item
from database_models import Document

def query_documents(field_name: str, field_value: Any, limit: int = 10) -> List[Document]:
    """
    Queries documents by a field value or partition-style key from AWS DynamoDB.
    This implementation assumes 'id' is the primary partition key, or 'status'
    is part of a Global Secondary Index (GSI) or Local Secondary Index (LSI).
    For non-indexed fields, a scan would be required, which is less efficient.
    """
    dynamodb = get_dynamodb_client()
    table_name = get_table_name()

    documents: List[Document] = []
    
    if field_name == "id":
        response = dynamodb.query(
            TableName=table_name,
            KeyConditionExpression=f"id = :val",
            ExpressionAttributeValues={":val": serialize_item({"v": field_value})["v"]},
            Limit=limit
        )
    elif field_name == "status":
        gsi_name = os.environ.get("DYNAMODB_STATUS_GSI_NAME", "StatusIndex")
        response = dynamodb.query(
            TableName=table_name,
            IndexName=gsi_name,
            KeyConditionExpression=f"status = :val",
            ExpressionAttributeValues={":val": serialize_item({"v": field_value})["v"]},
            Limit=limit
        )
    else:
        filter_expression_key = f"#{field_name}"
        filter_expression_value = f":val"
        
        response = dynamodb.scan(
            TableName=table_name,
            FilterExpression=f"{filter_expression_key} = {filter_expression_value}",
            ExpressionAttributeNames={filter_expression_key: field_name},
            ExpressionAttributeValues={filter_expression_value: serialize_item({"v": field_value})["v"]},
            Limit=limit
        )
            
    for item in response.get("Items", []):
        deserialized_item = deserialize_item(item)
        documents.append(Document(**deserialized_item))
            
    return documents
