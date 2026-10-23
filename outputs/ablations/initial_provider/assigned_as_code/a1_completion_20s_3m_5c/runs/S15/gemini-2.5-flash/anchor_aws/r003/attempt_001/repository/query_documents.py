import os
from decimal import Decimal
import json

import boto3
from boto3.dynamodb.conditions import Key

from database_client import get_dynamodb_client
from database_models import Document, QueryCondition


def query_documents(condition: QueryCondition, table_name: str, key_field: str = "id", index_name: str = None, region_name: str = None) -> list[Document]:
    dynamodb = get_dynamodb_client(region_name)
    table = dynamodb.Table(table_name)

    query_kwargs = {
        "KeyConditionExpression": Key(condition.field_name).eq(condition.field_value)
    }
    if index_name:
        query_kwargs["IndexName"] = index_name

    response = table.query(**query_kwargs)
    items = response.get("Items", [])

    documents = []
    for item in items:
        # Convert Decimal to float for JSON serialization if needed, or handle it as is.
        # For this example, we'll convert back to a regular dict, removing the key_field.
        doc_id = item.pop(key_field)
        # DynamoDB returns Decimal for numbers. Convert to float/int if that's the expected model.
        # A more robust solution might involve a custom JSON decoder for pydantic.
        # For simplicity, we convert Decimal to float/int in content if they exist.
        cleaned_content = json.loads(json.dumps(item, cls=DecimalEncoder))
        documents.append(Document(id=doc_id, content=cleaned_content))

    return documents


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            # Check if it's an integer (e.g., '10' rather than '10.0')
            if obj % 1 == 0:
                return int(obj)
            return float(obj)
        return super(DecimalEncoder, self).default(obj)
