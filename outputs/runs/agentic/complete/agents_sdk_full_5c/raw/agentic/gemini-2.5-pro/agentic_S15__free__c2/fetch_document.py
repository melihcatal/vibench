from typing import Dict, Any
from botocore.exceptions import ClientError
from database_client import get_boto_client, get_table_name

def fetch_document_by_id(document_id: str) -> Dict[str, Any]:
    """
    Fetches a single document from DynamoDB by its primary key.

    :param document_id: The ID of the document to fetch.
    :return: The document item if found, else None.
    """
    dynamodb = get_boto_client()
    table_name = get_table_name()

    try:
        response = dynamodb.get_item(
            TableName=table_name,
            Key={
                'documentId': {'S': document_id}
            }
        )
        item = response.get('Item')
        if item:
            print(f"Successfully fetched document {document_id}")
            return item
        else:
            print(f"Document {document_id} not found.")
            return None
    except ClientError as e:
        print(f"Error fetching document: {e.response['Error']['Message']}")
        return None
