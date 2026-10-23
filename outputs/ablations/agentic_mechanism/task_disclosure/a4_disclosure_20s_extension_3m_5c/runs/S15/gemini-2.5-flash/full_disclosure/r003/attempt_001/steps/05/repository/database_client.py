import os
import boto3

class DatabaseClient:
    def __init__(self):
        self.region_name = os.environ.get("AWS_REGION", "us-east-1")
        self.table_name = os.environ.get("DYNAMODB_TABLE_NAME", "my-nosql-table")
        self.dynamodb = self._get_dynamodb_client()

    def _get_dynamodb_client(self):
        return boto3.client("dynamodb", region_name=self.region_name)

    def get_table_name(self):
        return self.table_name

    def get_client(self):
        return self.dynamodb
