import os
import boto3
from botocore.exceptions import ClientError
from database_models import TABLE_NAME
from database_client import get_table

def upsert_document(document: dict):
    """
    Upserts a document into the Amazon DynamoDB table.

    :param document: The document to upsert. Must contain the primary key.
    :return: The response from DynamoDB.
    """
    if 'id' not in document:
        raise ValueError("Document must contain an 'id' key.")

    table = get_table(TABLE_NAME)
    try:
        response = table.put_item(
            Item=document
        )
        print(f"Successfully upserted document with id: {document['id']}")
        return response
    except ClientError as e:
        print(f"Error upserting document: {e.response['Error']['Message']}")
        raise
