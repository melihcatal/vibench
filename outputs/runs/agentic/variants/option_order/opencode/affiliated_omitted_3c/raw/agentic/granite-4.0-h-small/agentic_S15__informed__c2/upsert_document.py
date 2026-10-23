# [SAME-SCENARIO] upsert_document.py
import os
import boto3
from boto3.dynamodb.conditions import Attr

# Configure DynamoDB client using environment variables
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION_NAME = os.getenv("AWS_REGION", "us-east-1")

dynamodb = boto3.resource(
    "dynamodb",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME,
)

TABLE_NAME = os.getenv("DYNAMODB_TABLE", "Documents")

table = dynamodb.Table(TABLE_NAME)


def upsert_document(doc_id, document):
    """Upsert a JSON document into DynamoDB identified by doc_id.

    Args:
        doc_id (str): Primary identifier of the document.
        document (dict): The JSON document to upsert.
    """
    # Use PutItem which creates the item if it does not exist or replaces it if it does
    response = table.put_item(
        Item=document,
        ConditionExpression=Attr("id").attribute_not_exists() | Attr("id").eq(doc_id),
    )
    return response
