import os
import boto3
from typing import Dict, Any, Optional


class DynamoDBClient:
    """Client helper for Amazon DynamoDB operations." ""
    
    def __init__(self):
        self.dynamodb = boto3.resource(
            "dynamodb",
            region_name=os.getenv("AWS_REGION", "us-west-2"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )
        self.table_name = os.getenv("DYNAMODB_TABLE_NAME", "documents")
        self.table = self.dynamodb.Table(self.table_name)

    def get_table(self):
        """Returns the DynamoDB table resource." ""
        return self.table


def load_config() -> Dict[str, str]:
    """Loads configuration from environment variables." ""
    return {
        "aws_region": os.getenv("AWS_REGION", "us-west-2"),
        "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
        "dynamodb_table_name": os.getenv("DYNAMODB_TABLE_NAME", "documents"),
    }