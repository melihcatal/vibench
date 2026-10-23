import os
import json
from typing import Dict, Any, Optional
from database_client import get_dynamodb_client
from database_models import Document

def fetch_document(table_name: str, document_id: str) -> Optional[Document]:
    """
    Fetches a document by identifier from a managed NoSQL store (DynamoDB).
    
    Args:
        table_name: The name of the DynamoDB table.
        document_id: The primary identifier of the document to fetch.
        
    Returns:
        A Document object if found, otherwise None.
    """
    dynamodb = get_dynamodb_client()
    
    response = dynamodb.get_item(
        TableName=table_name,
        Key={
            'id': {'S': document_id}
        }
    )
    
    item = response.get('Item')
    if item:
        return Document.from_item(item)
    return None

if __name__ == "__main__":
    # Example Usage (requires AWS credentials and DynamoDB table configured)
    table_name = os.getenv("DYNAMODB_TABLE_NAME", "your-document-table")
    target_id = "doc123"
    
    print(f"Fetching document with ID: {target_id}")
    try:
        document = fetch_document(table_name, target_id)
        if document:
            print("Document fetched successfully:", json.dumps({"id": document.id, "data": document.data}, indent=2))
        else:
            print(f"Document with ID '{target_id}' not found.")
    except Exception as e:
        print(f"Error fetching document: {e}")
