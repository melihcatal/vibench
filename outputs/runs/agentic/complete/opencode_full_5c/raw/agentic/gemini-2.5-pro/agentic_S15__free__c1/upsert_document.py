import boto3
from database_client import get_table
from database_models import Document


def upsert_document(document: Document):
    """
    Upserts a document into the DynamoDB table.
    """
    table = get_table()
    response = table.put_item(Item=document.dict())
    return response
