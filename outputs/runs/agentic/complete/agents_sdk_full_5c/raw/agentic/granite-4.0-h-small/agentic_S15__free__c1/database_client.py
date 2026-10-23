import os
import boto3
from botocore.exceptions import BotoCoreError, ClientError

class NoSQLClient:
    """Thin wrapper around Amazon DynamoDB providing helper methods.

    All method calls require the environment variable DYNAMODB_TABLE to be set.
    """
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(os.getenv('DYNAMODB_TABLE'))

    def put_item(self, **kwargs):
        """Wrapper for Table.put_item that handles serialization errors."""
        try:
            self.table.put_item(Item=kwargs)
        except ClientError as e:
            raise RuntimeError(f"DynamoDB put_item failed: {e}")

    def get_item(self, **kwargs):
        try:
            return self.table.get_item(**kwargs)
        except ClientError as e:
            raise RuntimeError(f"DynamoDB get_item failed: {e}")

    def query(self, **kwargs):
        try:
            return self.table.query(**kwargs)
        except ClientError as e:
            raise RuntimeError(f"DynamoDB query failed: {e}")

    def update_item(self, **kwargs):
        try:
            return self.table.update_item(**kwargs)
        except ClientError as e:
            raise RuntimeError(f"DynamoDB update_item failed: {e}")
