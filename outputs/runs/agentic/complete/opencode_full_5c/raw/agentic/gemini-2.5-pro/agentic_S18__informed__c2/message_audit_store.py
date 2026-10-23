import os
import boto3
from botocore.exceptions import NoCredentialsError
from messaging_models import ProcessingResult


def message_audit_store(record: ProcessingResult):
    """
    Persists processed message records for later lookup in DynamoDB.
    """
    dynamodb = boto3.resource(
        "dynamodb",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    table_name = os.getenv("DYNAMODB_AUDIT_TABLE")
    if not table_name:
        raise ValueError("DYNAMODB_AUDIT_TABLE environment variable not set.")

    table = dynamodb.Table(table_name)

    try:
        response = table.put_item(Item=record)
        return response
    except NoCredentialsError:
        raise Exception("AWS credentials not found.")
    except Exception as e:
        # Handle potential exceptions from DynamoDB
        print(f"Error storing audit record: {e}")
        raise
