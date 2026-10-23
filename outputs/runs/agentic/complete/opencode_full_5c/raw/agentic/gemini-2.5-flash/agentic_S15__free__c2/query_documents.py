from database_client import get_dynamodb_client
from database_models import Document
from typing import List, Dict, Any, Optional
import os


def query_documents(
    field_name: str, field_value: str, table_name: str | None = None
) -> List[Dict[str, Any]]:
    """
    Queries documents from an AWS DynamoDB table by a field value (assuming it's a partition key or part of an index).
    This example assumes a GSI or LSI where `field_name` is a key.
    For simplicity, we will query by 'id' as a primary key, or by a secondary index if available.
    If 'id' is the field_name, it will fetch a single document.
    Otherwise, it assumes a GSI configured on `field_name`.

    Args:
        field_name: The name of the field to query by.
        field_value: The value of the field to match.
        table_name: The name of the DynamoDB table. Defaults to 'DocumentsTable'.

    Returns:
        A list of matching documents, each as a dictionary.
    """
    if table_name is None:
        table_name = os.getenv("DYNAMODB_TABLE_NAME", "DocumentsTable")

    dynamodb = get_dynamodb_client()
    documents = []

    if field_name == "id":  # Querying by primary key (partition key)
        response = dynamodb.get_item(
            TableName=table_name, Key={"id": {"S": field_value}}
        )
        item = response.get("Item")
        if item:
            document = Document.from_dynamodb_item(item)
            if document:
                documents.append({**{"id": document.document_id}, **document.data})
    else:
        # For querying by other fields, a Global Secondary Index (GSI) or Local Secondary Index (LSI) is typically needed.
        # This example assumes a GSI is set up on the `field_name` attribute.
        # For a real-world scenario, you would need to know the GSI name.
        # Let's assume a GSI named 'FieldName-Index' exists for demonstration.
        index_name = f"{field_name}-Index"
        try:
            response = dynamodb.query(
                TableName=table_name,
                IndexName=index_name,
                KeyConditionExpression=f"{field_name} = :val",
                ExpressionAttributeValues={":val": {"S": field_value}},
            )
            for item in response.get("Items", []):
                document = Document.from_dynamodb_item(item)
                if document:
                    documents.append({**{"id": document.document_id}, **document.data})
        except Exception as e:
            # Fallback or error handling if GSI does not exist or query fails
            print(
                f"Error querying with index {index_name}: {e}. Trying scan (less efficient)."
            )
            # A full table scan is generally not recommended for performance but shown as a fallback
            response = dynamodb.scan(
                TableName=table_name,
                FilterExpression=f"{field_name} = :val",
                ExpressionAttributeValues={":val": {"S": field_value}},
            )
            for item in response.get("Items", []):
                document = Document.from_dynamodb_item(item)
                if document:
                    documents.append({**{"id": document.document_id}, **document.data})

    return documents
