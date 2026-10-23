# [HELPER] database_client.py
import os
import boto3

# Load DynamoDB credentials from environment variables
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION_NAME = os.getenv("AWS_REGION", "us-east-1")


# Helper to instantiate a DynamoDB client/resource in one place
class DynamoDBClient:
    @staticmethod
    def get_resource():
        return boto3.resource(
            "dynamodb",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=REGION_NAME,
        )

    @staticmethod
    def get_client():
        return boto3.client(
            "dynamodb",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=REGION_NAME,
        )
