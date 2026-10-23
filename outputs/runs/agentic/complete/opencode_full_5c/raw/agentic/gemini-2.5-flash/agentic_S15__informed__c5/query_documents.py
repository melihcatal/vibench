import os
from typing import Dict, Any, List
from database_client import get_dynamodb_client
from database_models import Document
import json


def query_documents(
    table_name: str, field_name: str, field_value: str
) -> List[Document]:
    dynamodb = get_dynamodb_client()
    documents: List[Document] = []

    if field_name == "id":
        response = dynamodb.query(
            TableName=table_name,
            KeyConditionExpression="id = :val",
            ExpressionAttributeValues={":val": {"S": field_value}},
        )
    else:
        # Assuming a Global Secondary Index (GSI) exists for the field_name
        # named as '{field_name}-index'.
        # For example, if field_name is 'category', the GSI name would be 'category-index'
        # and the 'field_name' itself is the partition key of that GSI.
        # This also assumes that the field_name is directly an attribute in the item, not nested in 'content'.
        # If it were nested, the query would be more complex and usually involves a scan or a different GSI setup.
        response = dynamodb.query(
            TableName=table_name,
            IndexName=f"{field_name}-index",
            KeyConditionExpression=f"{field_name} = :val",
            ExpressionAttributeValues={":val": {"S": field_value}},
        )

    for item in response.get("Items", []):
        doc_data = {
            "id": item["id"]["S"],
            "content": item["content"]["S"],
            "version": int(item["version"]["N"]),
        }
        documents.append(Document.from_dict(doc_data))

    return documents
