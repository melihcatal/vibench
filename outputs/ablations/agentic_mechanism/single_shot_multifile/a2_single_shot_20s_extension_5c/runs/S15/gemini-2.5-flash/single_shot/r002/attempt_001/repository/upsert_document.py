import os
import json
from database_client import get_dynamodb_client, get_table_name

def upsert_document(document_id: str, document_data: dict):
    dynamodb = get_dynamodb_client()
    table_name = get_table_name()

    item = {
        'id': document_id
    }
    item.update(document_data)

    try:
        response = dynamodb.put_item(
            TableName=table_name,
            Item=item
        )
        return {"status": "success", "response": response}
    except Exception as e:
        return {"status": "error", "message": str(e)}
