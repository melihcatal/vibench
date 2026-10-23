import os
from typing import Optional, Dict, Any
from boto3 import client as boto3_client
from botocore.exceptions import ClientError
import json


class DynamoDBClient:
    """Client helper utilities for AWS DynamoDB."""

    def __init__(self, table_name: Optional[str] = None):
        """
        Initialize DynamoDB client.

        Args:
            table_name: Optional default table name
        """
        self.table_name = table_name or os.environ.get("DYNAMODB_TABLE", "documents")
        self._client = None

    @property
    def client(self):
        """Lazy initialization of DynamoDB client."""
        if self._client is None:
            self._client = boto3_client(
                "dynamodb",
                aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
                region_name=os.environ.get("AWS_REGION", "us-east-1"),
            )
        return self._client

    def get_config(self) -> Dict[str, Any]:
        """Get current DynamoDB configuration."""
        return {
            "provider": "aws:dynamodb",
            "table": self.table_name,
            "region": os.environ.get("AWS_REGION", "us-east-1"),
            "access_key_id": os.environ.get("AWS_ACCESS_KEY_ID", "not-set")[:8] + "..."
            if os.environ.get("AWS_ACCESS_KEY_ID")
            else None,
        }

    def health_check(self) -> Dict[str, Any]:
        """Check if DynamoDB is accessible."""
        try:
            # Try to describe the table
            response = self.client.describe_table(TableName=self.table_name)
            table_status = response["Table"]["TableStatus"]

            return {
                "success": True,
                "status": "healthy",
                "table_status": table_status,
                "provider": "aws:dynamodb",
            }
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "ResourceNotFoundException":
                return {
                    "success": False,
                    "status": "table_not_found",
                    "error": f"Table {self.table_name} not found",
                    "provider": "aws:dynamodb",
                }
            return {
                "success": False,
                "status": "unhealthy",
                "error": str(e),
                "provider": "aws:dynamodb",
            }
        except Exception as e:
            return {
                "success": False,
                "status": "error",
                "error": f"Unexpected error: {str(e)}",
                "provider": "aws:dynamodb",
            }

    def normalize_document(self, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize document data for storage.

        Args:
            document_data: Raw document data

        Returns:
            Normalized document with metadata
        """
        normalized = document_data.copy()

        # Add metadata if not present
        if "_created_at" not in normalized:
            normalized["_created_at"] = os.environ.get(
                "TIMESTAMP", "2025-01-01T00:00:00Z"
            )

        if "_updated_at" not in normalized:
            normalized["_updated_at"] = os.environ.get(
                "TIMESTAMP", "2025-01-01T00:00:00Z"
            )

        if "_version" not in normalized:
            normalized["_version"] = 1

        return normalized

    def parse_dynamo_item(self, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Parse DynamoDB item to Python dictionary.

        Args:
            item: DynamoDB item response

        Returns:
            Parsed document or None if invalid
        """
        try:
            if "id" not in item or "data" not in item:
                return None

            document_id = item["id"]["S"]
            document_data = json.loads(item["data"]["S"])

            result = {
                "id": document_id,
                "data": document_data,
                "provider": "aws:dynamodb",
            }

            # Add optional metadata fields
            if "updated_at" in item:
                result["updated_at"] = item["updated_at"]["S"]

            return result
        except (KeyError, json.JSONDecodeError):
            return None

    def create_table_if_not_exists(
        self, table_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create DynamoDB table if it doesn't exist.

        Args:
            table_name: Table name (uses default if not specified)

        Returns:
            Creation result
        """
        target_table = table_name or self.table_name

        try:
            # Check if table exists
            self.client.describe_table(TableName=target_table)
            return {
                "success": True,
                "action": "table_exists",
                "table": target_table,
                "provider": "aws:dynamodb",
            }
        except ClientError as e:
            if e.response["Error"]["Code"] != "ResourceNotFoundException":
                return {"success": False, "error": str(e), "provider": "aws:dynamodb"}

        # Create table
        try:
            response = self.client.create_table(
                TableName=target_table,
                KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
                AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
                BillingMode="PAY_PER_REQUEST",
            )

            return {
                "success": True,
                "action": "table_created",
                "table": target_table,
                "table_status": response["TableDescription"]["TableStatus"],
                "provider": "aws:dynamodb",
            }
        except ClientError as e:
            return {"success": False, "error": str(e), "provider": "aws:dynamodb"}
