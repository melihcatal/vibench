from database_client import get_dynamodb_client
from database_models import Document
import os


def query_documents_by_field(field_name: str, field_value: str) -> list[Document]:
    """
    Queries documents by a field value or partition-style key from AWS DynamoDB.
    Assumes a GSI or LSI exists for the field_name if it's not the primary key.
    """
    dynamodb = get_dynamodb_client()
    table_name = os.environ.get(
        "DYNAMODB_TABLE_NAME", "your-document-table"
    )  # AWS DynamoDB
    index_name = os.environ.get(
        "DYNAMODB_GSI_NAME", f"{field_name}Index"
    )  # Example GSI Name

    # This example assumes `field_name` is a Partition Key for an existing GSI.
    # For a simple query on a non-key attribute, a Scan would be used, but Query is more efficient.
    # This assumes an index exists on `field_name`.
    try:
        response = dynamodb.query(
            TableName=table_name,
            IndexName=index_name,  # AWS DynamoDB
            KeyConditionExpression=f"{field_name} = :val",
            ExpressionAttributeValues={":val": {"S": field_value}},
        )
    except dynamodb.exceptions.ResourceNotFoundException:
        # Fallback to scan if GSI is not found or not suitable for simple attribute query
        # In a real-world scenario, you'd define and use appropriate GSIs.
        print(f"Index {index_name} not found, performing a scan (less efficient).")
        response = dynamodb.scan(
            TableName=table_name,
            FilterExpression=f"{field_name} = :val",
            ExpressionAttributeValues={":val": {"S": field_value}},
        )

    documents = []
    for item in response.get("Items", []):
        documents.append(Document.from_dynamodb_item(item))
    return documents
