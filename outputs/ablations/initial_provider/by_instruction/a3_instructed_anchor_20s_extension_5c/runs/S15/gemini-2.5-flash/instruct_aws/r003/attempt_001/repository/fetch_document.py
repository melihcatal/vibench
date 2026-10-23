import os
from database_client import get_dynamodb_client
from database_models import Document

TABLE_NAME = os.environ.get("DYNAMODB_TABLE_NAME", "your-dynamodb-table-name")

def fetch_document(document_id: str):
    dynamodb = get_dynamodb_client()

    try:
        response = dynamodb.get_item(
            TableName=TABLE_NAME,
            Key={
                "id": {"S": document_id}
            }
        )
        item = response.get("Item")
        if item:
            return {"status": "success", "document": Document.from_item(item).content}
        else:
            return {"status": "not_found", "message": f"Document with id {document_id} not found."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
