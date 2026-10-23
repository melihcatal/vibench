import os
from typing import Dict, Any
from database_client import get_dynamodb_client
from database_models import Document


def upsert_document(table_name: str, document: Document) -> Dict[str, Any]:
    dynamodb = get_dynamodb_client()
    item = document.to_dict()

    response = dynamodb.put_item(
        TableName=table_name,
        Item={
            "id": {"S": item["id"]},
            "content": {"S": item["content"]},
            "version": {"N": str(item["version"])},
        },
    )
    return response
