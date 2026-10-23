import os
from botocore.exceptions import ClientError
from database_models import TABLE_NAME
from database_client import get_table

def fetch_document(doc_id: str):
    """
    Fetches a document from the Amazon DynamoDB table by its ID.

    :param doc_id: The ID of the document to fetch.
    :return: The document item if found, otherwise None.
    """
    table = get_table(TABLE_NAME)
    try:
        response = table.get_item(
            Key={
                'id': doc_id
            }
        )
        item = response.get('Item')
        if item:
            print(f"Successfully fetched document with id: {doc_id}")
            return item
        else:
            print(f"Document with id: {doc_id} not found.")
            return None
    except ClientError as e:
        print(f"Error fetching document: {e.response['Error']['Message']}")
        raise
