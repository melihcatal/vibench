import os
from database_client import get_dynamodb_client, get_table_name

def fetch_document(document_id: str):
    dynamodb = get_dynamodb_client()
    table_name = get_table_name()

    try:
        response = dynamodb.get_item(
            TableName=table_name,
            Key={
                'id': document_id
            }
        )
        item = response.get('Item')
        if item:
            return {"status": "success", "document": item}
        else:
            return {"status": "not_found", "message": "Document not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
