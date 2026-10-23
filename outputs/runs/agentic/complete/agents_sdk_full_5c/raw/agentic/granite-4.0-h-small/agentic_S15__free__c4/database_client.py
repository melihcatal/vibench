# [HELPER] database_client.py
import os
import json
import boto3
from botocore.exceptions import ClientError

class NoSQLClient:
    """Encapsulate a managed NoSQL (DynamoDB) client and table metadata."""

    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        # Pull table name from environment or use a fixed default
        self.table_name = os.getenv('DYNAMODB_TABLE', 'my-documents')
        self.table = self.dynamodb.Table(self.table_name)

    def put_item(self, **kwargs):
        return self.table.put_item(**kwargs)

    def get_item(self, **kwargs):
        return self.table.get_item(**kwargs)

    def query(self, **kwargs):
        return self.table.query(**kwargs)

    def update_item(self, **kwargs):
        return self.table.update_item(**kwargs)

    def key_condition(self, partition_key):
        return NoSQLClient._key_condition(partition_key)

    def attribute_name(self, attr):
        return NoSQLClient._attribute_name(attr)

    @staticmethod
    def _key_condition(partition_key):
        return f"{partition_key} = :pk"

    @staticmethod
    def _attribute_name(attr):
        return f"#{attr}"