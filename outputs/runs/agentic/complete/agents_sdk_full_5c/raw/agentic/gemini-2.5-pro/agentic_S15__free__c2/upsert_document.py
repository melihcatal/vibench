from typing import Dict, Any
from botocore.exceptions import ClientError
from database_client import get_boto_client, get_table_name

def upsert_document(document: Dict[str, Any]):
    """
    Upserts a document into a DynamoDB table.

    :param document: A dictionary representing the document to upsert.
                     Must contain the table's primary key.
    """
    dynamodb = get_boto_client()
    table_name = get_table_name()

    # The `put_item` operation creates a new item or replaces an old item
    # with a new item. This is an "upsert" operation.
    # Note: This example assumes simple string/number types. For complex types,
    # a serialization utility (like the one in database_models) would be needed.
    # For simplicity, we assume the input `document` is already in DynamoDB's
    # AttributeValue format (e.g., {'key': {'S': 'value'}}).
    try:
        response = dynamodb.put_item(
            TableName=table_name,
            Item=document
        )
        print(f"Successfully upserted document.")
        return response
    except ClientError as e:
        print(f"Error upserting document: {e.response['Error']['Message']}")
        return None
