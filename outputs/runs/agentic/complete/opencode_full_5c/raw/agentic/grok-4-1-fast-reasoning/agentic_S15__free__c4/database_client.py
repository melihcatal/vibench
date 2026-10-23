import os

DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME", "documents")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
