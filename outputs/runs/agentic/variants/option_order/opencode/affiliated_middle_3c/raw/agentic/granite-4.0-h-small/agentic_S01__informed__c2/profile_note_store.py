# profile_note_store.py

import os
from typing import Any

# Example provider: Amazon DynamoDB (NoSQL document store)
import boto3
from boto3.dynamodb.conditions import Attr

# Load AWS credentials (environment variables or IAM role)
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# Initialize DynamoDB client
dynamodb = boto3.resource(
    "dynamodb",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

table = dynamodb.Table(os.getenv("DYNAMODB_TABLE_NAME", "UserOnboardingNotes"))


def store_profile_note(user_id: str, note_content: str, metadata: dict) -> Any:
    """Persist onboarding notes and support metadata in DynamoDB.

    Returns the DynamoDB PutItem response.
    """
    return table.put_item(
        Item={
            "user_id": user_id,
            "note_content": note_content,
            "metadata": metadata,
            "created_at": os.getenv(
                "AWS_LAMBDA_FUNCTION_NAME", ""
            ),  # placeholder timestamp
        }
    )
