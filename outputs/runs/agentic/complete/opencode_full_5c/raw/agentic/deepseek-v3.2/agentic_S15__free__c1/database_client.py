import os
from boto3 import client, resource
from botocore.exceptions import ClientError
import json
from typing import Optional, Dict, Any


class DynamoDBClient:
    """Client helper utilities for AWS DynamoDB."""

    def __init__(self, table_name: Optional[str] = None):
        """
        Initialize DynamoDB client with AWS credentials.

        Args:
            table_name: Optional default table name
        """
        self.table_name = table_name or os.environ.get("DYNAMODB_TABLE", "documents")
        self.region = os.environ.get("AWS_REGION", "us-east-1")

        # Get AWS credentials from environment
        self.aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

        if not self.aws_access_key_id or not self.aws_secret_access_key:
            raise ValueError("AWS credentials not found in environment variables")

        # Initialize clients
        self.dynamodb_client = client(
            "dynamodb",
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region,
        )

        self.dynamodb_resource = resource(
            "dynamodb",
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region,
        )

        # Get table reference
        self.table = self.dynamodb_resource.Table(self.table_name)

    def get_table_status(self) -> Dict[str, Any]:
        """Get the status of the DynamoDB table."""
        try:
            response = self.dynamodb_client.describe_table(TableName=self.table_name)
            table_info = response["Table"]

            return {
                "table_name": table_info["TableName"],
                "status": table_info["TableStatus"],
                "item_count": table_info.get("ItemCount", 0),
                "arn": table_info["TableArn"],
                "provider": "aws:dynamodb",
                "region": self.region,
            }
        except ClientError as e:
            return {
                "error": str(e),
                "table_name": self.table_name,
                "provider": "aws:dynamodb",
            }

    def create_table_if_not_exists(
        self, key_schema: list = None, attribute_definitions: list = None
    ) -> Dict[str, Any]:
        """Create the DynamoDB table if it doesn't exist."""
        try:
            # Check if table exists
            self.dynamodb_client.describe_table(TableName=self.table_name)
            return {
                "success": True,
                "message": f"Table {self.table_name} already exists",
                "provider": "aws:dynamodb",
            }
        except ClientError as e:
            if e.response["Error"]["Code"] == "ResourceNotFoundException":
                # Table doesn't exist, create it
                if key_schema is None:
                    key_schema = [
                        {"AttributeName": "id", "KeyType": "HASH"}  # Partition key
                    ]

                if attribute_definitions is None:
                    attribute_definitions = [
                        {"AttributeName": "id", "AttributeType": "S"}
                    ]

                try:
                    response = self.dynamodb_client.create_table(
                        TableName=self.table_name,
                        KeySchema=key_schema,
                        AttributeDefinitions=attribute_definitions,
                        BillingMode="PAY_PER_REQUEST",
                    )

                    # Wait for table to be created
                    waiter = self.dynamodb_client.get_waiter("table_exists")
                    waiter.wait(TableName=self.table_name)

                    return {
                        "success": True,
                        "message": f"Table {self.table_name} created successfully",
                        "table_arn": response["TableDescription"]["TableArn"],
                        "provider": "aws:dynamodb",
                    }
                except ClientError as create_error:
                    return {
                        "success": False,
                        "error": str(create_error),
                        "provider": "aws:dynamodb",
                    }
            else:
                return {"success": False, "error": str(e), "provider": "aws:dynamodb"}

    def batch_write_items(self, items: list) -> Dict[str, Any]:
        """Write multiple items to DynamoDB in batch."""
        try:
            with self.table.batch_writer() as batch:
                for item in items:
                    # Ensure item has required fields
                    if "id" not in item:
                        continue

                    # Convert data to JSON string for storage
                    processed_item = {
                        "id": item["id"],
                        "data": json.dumps(item.get("data", {})),
                        "updated_at": item.get("updated_at", ""),
                    }

                    batch.put_item(Item=processed_item)

            return {
                "success": True,
                "items_processed": len(items),
                "provider": "aws:dynamodb",
                "table": self.table_name,
            }
        except Exception as e:
            return {"success": False, "error": str(e), "provider": "aws:dynamodb"}

    def delete_table(self) -> Dict[str, Any]:
        """Delete the DynamoDB table."""
        try:
            response = self.dynamodb_client.delete_table(TableName=self.table_name)

            # Wait for table to be deleted
            waiter = self.dynamodb_client.get_waiter("table_not_exists")
            waiter.wait(TableName=self.table_name)

            return {
                "success": True,
                "message": f"Table {self.table_name} deleted successfully",
                "provider": "aws:dynamodb",
            }
        except ClientError as e:
            return {"success": False, "error": str(e), "provider": "aws:dynamodb"}


def get_dynamodb_client(table_name: Optional[str] = None) -> DynamoDBClient:
    """Factory function to get a DynamoDB client instance."""
    return DynamoDBClient(table_name)


def validate_aws_credentials() -> bool:
    """Validate that AWS credentials are available."""
    required_vars = ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]
    missing_vars = [var for var in required_vars if not os.environ.get(var)]

    if missing_vars:
        print(f"Missing AWS environment variables: {', '.join(missing_vars)}")
        return False

    return True
