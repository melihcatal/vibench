from typing import Dict, Any, Optional
import boto3
from database_client import get_dynamodb_table

def fetch_document(document_id: str) -> Optional[Dict[str, Any]]:
    table = get_dynamodb_table()
    response = table.get_item(Key={"id": document_id})
    return response.get("Item")