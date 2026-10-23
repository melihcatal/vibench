import os
from boto3 import client, resource
from botocore.exceptions import ClientError
import json
from typing import Optional, Dict, Any


class DynamoDBClient:
    """Client helper utilities for AWS DynamoDB."""

    def __init__(self, table_name: str = None):
        """
        Initialize DynamoDB client.

        Args:
            table_name: Optional default table name
        """
        self.table_name = table_name or os.environ.get("DYNAMODB_TABLE", "documents")
        self.region = os.environ.get("AWS_REGION", "us-east-1")

        self.dynamodb_client = client(
            "dynamodb",
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            region_name=self.region,
        )

        self.dynamodb_resource = resource(
            "dynamodb",
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            region_name=self.region,
        )

    def get_table(self):
        """Get DynamoDB table resource."""
        return self.dynamodb_resource.Table(self.table_name)

    def create_table_if_not_exists(
        self,
        partition_key: str = "document_id",
        sort_key: str = None,
        read_capacity: int = 5,
        write_capacity: int = 5,
    ):
        """
        Create DynamoDB table if it doesn't exist.

        Args:
            partition_key: Partition key name
            sort_key: Optional sort key name
            read_capacity: Read capacity units
            write_capacity: Write capacity units
        """
        try:
            existing_tables = self.dynamodb_client.list_tables()["TableNames"]
            if self.table_name in existing_tables:
                return

            key_schema = [{"AttributeName": partition_key, "KeyType": "HASH"}]
            attribute_definitions = [
                {"AttributeName": partition_key, "AttributeType": "S"}
            ]

            if sort_key:
                key_schema.append({"AttributeName": sort_key, "KeyType": "RANGE"})
                attribute_definitions.append(
                    {"AttributeName": sort_key, "AttributeType": "S"}
                )

            self.dynamodb_client.create_table(
                TableName=self.table_name,
                KeySchema=key_schema,
                AttributeDefinitions=attribute_definitions,
                ProvisionedThroughput={
                    "ReadCapacityUnits": read_capacity,
                    "WriteCapacityUnits": write_capacity,
                },
            )

            # Wait for table to be created
            waiter = self.dynamodb_client.get_waiter("table_exists")
            waiter.wait(TableName=self.table_name)

        except ClientError as e:
            if e.response["Error"]["Code"] != "ResourceInUseException":
                raise

    def batch_write_items(self, items: list):
        """
        Write multiple items in batch.

        Args:
            items: List of items to write
        """
        table = self.get_table()
        with table.batch_writer() as batch:
            for item in items:
                batch.put_item(Item=item)

    def scan_table(self, limit: int = 100):
        """
        Scan table with optional limit.

        Args:
            limit: Maximum number of items to return

        Returns:
            List of items
        """
        table = self.get_table()
        response = table.scan(Limit=limit)
        return response.get("Items", [])
