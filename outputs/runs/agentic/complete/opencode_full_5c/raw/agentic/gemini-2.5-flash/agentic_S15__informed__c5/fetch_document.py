import os
from typing import Dict, Any, Optional
from database_client import get_dynamodb_client
from database_models import Document


def fetch_document(table_name: str, document_id: str) -> Optional[Document]:
    dynamodb = get_dynamodb_client()
    response = dynamodb.get_item(TableName=table_name, Key={"id": {"S": document_id}})
    item = response.get("Item")
    if item:
        # Convert DynamoDB item format back to a dictionary suitable for Document.from_dict
        doc_data = {
            "id": item["id"]["S"],
            "content": item["content"]["S"],
            "version": int(item["version"]["N"]),
        }
        return Document.from_dict(doc_data)
    return None
