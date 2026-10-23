from database_client import get_db_table
from botocore.exceptions import ClientError
from typing import Optional, Dict

def fetch_document(table_name: str, document_id: str) -> Optional[Dict]:
    """
    Fetches a document by its ID from an Amazon DynamoDB table.

    :param table_name: The name of the DynamoDB table.
    :param document_id: The ID of the document to fetch.
    :return: The document item if found, otherwise None.
    """
    table = get_db_table(table_name)
    if not table:
        raise ConnectionError("Could not connect to the database.")

    try:
        response = table.get_item(
            Key={
                'id': document_id
            }
        )
        return response.get('Item')
    except ClientError as e:
        print(f"Error fetching document {document_id}: {e.response['Error']['Message']}")
        raise
