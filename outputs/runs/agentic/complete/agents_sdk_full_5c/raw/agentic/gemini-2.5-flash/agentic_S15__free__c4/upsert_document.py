import os
import json
from typing import Dict, Any
from database_client import get_dynamodb_client
from database_models import Document

def upsert_document(table_name: str, document: Document) -> Dict[str, Any]:
    """
    Upserts a JSON document into the specified DynamoDB table by its primary identifier.
    
    Args:
        table_name: The name of the DynamoDB table.
        document: The Document object to upsert.
        
    Returns:
        The response from the DynamoDB put_item operation.
    """
    dynamodb = get_dynamodb_client()
    
    item = document.to_item()

    response = dynamodb.put_item(
        TableName=table_name,
        Item=item
    )
    return response

if __name__ == "__main__":
    # Example Usage (requires AWS credentials and DynamoDB table configured)
    table_name = os.getenv("DYNAMODB_TABLE_NAME", "your-document-table")
    sample_doc = Document(
        id="doc123",
        data={
            "title": "My First Document",
            "author": "Jane Doe",
            "content": "This is the content of my first document.",
            "version": 1,
            "isPublished": True
        }
    )
    
    print(f"Upserting document with ID: {sample_doc.id}")
    try:
        response = upsert_document(table_name, sample_doc)
        print("Document upserted successfully:", json.dumps(response, indent=2))
    except Exception as e:
        print(f"Error upserting document: {e}")
