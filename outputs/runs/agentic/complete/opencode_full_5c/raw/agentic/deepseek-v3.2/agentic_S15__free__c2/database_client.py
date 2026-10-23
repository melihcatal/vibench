import os
from typing import Optional, Dict, Any
from boto3 import client as boto3_client
from botocore.config import Config


class DynamoDBClient:
    """Client helper utilities for AWS DynamoDB."""

    def __init__(self, table_name: Optional[str] = None):
        """
        Initialize DynamoDB client with configuration from environment.

        Args:
            table_name: Optional default table name
        """
        self.table_name = table_name or os.environ.get("DYNAMODB_TABLE_NAME")
        self.region = os.environ.get("AWS_REGION", "us-east-1")

        # Configure retry behavior
        config = Config(retries={"max_attempts": 3, "mode": "standard"})

        # Initialize client
        self.client = boto3_client(
            "dynamodb",
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            region_name=self.region,
            config=config,
        )

    def get_table_info(self) -> Dict[str, Any]:
        """Get information about the configured table."""
        try:
            if not self.table_name:
                raise ValueError("No table name configured")

            response = self.client.describe_table(TableName=self.table_name)
            table_info = response.get("Table", {})

            return {
                "table_name": table_info.get("TableName"),
                "table_status": table_info.get("TableStatus"),
                "item_count": table_info.get("ItemCount", 0),
                "table_size_bytes": table_info.get("TableSizeBytes", 0),
                "creation_date": table_info.get("CreationDateTime"),
                "key_schema": table_info.get("KeySchema", []),
                "provisioned_throughput": table_info.get("ProvisionedThroughput", {}),
            }
        except Exception as e:
            return {"error": str(e), "table_name": self.table_name}

    def health_check(self) -> Dict[str, Any]:
        """Perform a health check on the DynamoDB connection."""
        try:
            # Simple list_tables call to verify connectivity
            response = self.client.list_tables(Limit=1)

            return {
                "healthy": True,
                "service": "dynamodb",
                "region": self.region,
                "tables_accessible": True,
                "table_count": len(response.get("TableNames", [])),
            }
        except Exception as e:
            return {
                "healthy": False,
                "service": "dynamodb",
                "region": self.region,
                "error": str(e),
            }

    @staticmethod
    def validate_aws_credentials() -> bool:
        """Validate that AWS credentials are configured."""
        required_vars = ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]
        return all(os.environ.get(var) for var in required_vars)

    @staticmethod
    def get_configuration() -> Dict[str, Any]:
        """Get current DynamoDB configuration from environment."""
        return {
            "aws_region": os.environ.get("AWS_REGION", "us-east-1"),
            "table_name": os.environ.get("DYNAMODB_TABLE_NAME"),
            "credentials_configured": DynamoDBClient.validate_aws_credentials(),
            "endpoint_url": os.environ.get(
                "DYNAMODB_ENDPOINT_URL"
            ),  # For local testing
        }


# Factory function for creating clients
def create_dynamodb_client(table_name: Optional[str] = None) -> DynamoDBClient:
    """
    Create a DynamoDB client instance.

    Args:
        table_name: Optional table name to use

    Returns:
        DynamoDBClient instance
    """
    return DynamoDBClient(table_name)
