import os
from typing import Dict, Any, Optional
import boto3
from botocore.exceptions import ClientError

def get_dynamodb_table():
    dynamodb = boto3.resource(
        "dynamodb",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    return dynamodb.Table(os.getenv("DYNAMODB_TABLE_NAME", "Documents"))


def conditional_update(
    document_id: str, 
    update_expression: str, 
    condition_expression: str, 
    expression_values: Dict[str, Any]
) -> bool:
    table = get_dynamodb_table()
    try:
        response = table.update_item(
            Key={"document_id": document_id},
            UpdateExpression=update_expression,
            ConditionExpression=condition_expression,
            ExpressionAttributeValues=expression_values,
            ReturnValues="UPDATED_NEW"
        )
        return response.get("Attributes") is not None
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            print("Condition check failed, update not applied")
        else:
            print(f"Error updating document: {e}")
        return False