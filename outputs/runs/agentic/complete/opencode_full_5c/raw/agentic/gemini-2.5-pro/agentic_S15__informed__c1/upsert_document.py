import boto3
from database_client import get_db_table
from database_models import Document


def upsert_document(document: Document):
    """
    Upserts a document into DynamoDB.

    :param document: A dictionary representing the document.
    """
    table = get_db_table()
    response = table.put_item(Item=document)
    return response
