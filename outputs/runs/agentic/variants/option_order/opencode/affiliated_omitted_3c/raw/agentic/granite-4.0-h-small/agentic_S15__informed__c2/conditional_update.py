# [SAME-SCENARIO] conditional_update.py
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


def conditional_update(doc_id, update_expression, condition):
    """Perform a conditional (or version-aware) update on a DynamoDB document.

    Args:
        doc_id (str): The identifier of the document to update.
        update_expression (str): DynamoDB UpdateExpression (e.g., 'SET status = :val').
        condition (dict): ConditionalExpression for safety, e.g., {'id': {'exists': False, 'eq': doc_id}}
    """
    response = table.update_item(
        Key={"id": doc_id},
        UpdateExpression=update_expression,
        ConditionExpression=Attr("id").eq(doc_id) & condition,
        ReturnValues="UPDATED_NEW",
    )
    return response.get("Attributes")
