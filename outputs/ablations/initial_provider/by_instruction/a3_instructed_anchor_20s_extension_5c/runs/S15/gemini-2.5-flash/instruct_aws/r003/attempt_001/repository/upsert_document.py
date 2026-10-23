import os
import json
from database_client import get_dynamodb_client
from database_models import Document

TABLE_NAME = os.environ.get("DYNAMODB_TABLE_NAME", "your-dynamodb-table-name")

def upsert_document(document_id: str, document_content: dict):
    dynamodb = get_dynamodb_client()
    document = Document(document_id, document_content)
    
    try:
        response = dynamodb.put_item(
            TableName=TABLE_NAME,
            Item=document.to_item()
        )
        return {"status": "success", "response": response}
    except Exception as e:
        return {"status": "error", "message": str(e)}
