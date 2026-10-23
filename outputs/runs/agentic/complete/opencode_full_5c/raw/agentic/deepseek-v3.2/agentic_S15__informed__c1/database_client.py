import os
import boto3
from botocore.config import Config
from typing import Optional

# DynamoDB configuration
DYNAMODB_TABLE_NAME = os.environ.get("DYNAMODB_TABLE_NAME", "documents")
DYNAMODB_REGION = os.environ.get("AWS_REGION", "us-east-1")
DYNAMODB_ENDPOINT_URL = os.environ.get("DYNAMODB_ENDPOINT_URL")  # For local testing

# AWS credentials from environment
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_SESSION_TOKEN = os.environ.get("AWS_SESSION_TOKEN")

# Client cache
_dynamodb_client = None
_dynamodb_resource = None


def get_dynamodb_client():
    """
    Get or create a DynamoDB client with proper configuration.
    """
    global _dynamodb_client

    if _dynamodb_client is None:
        config = Config(retries={"max_attempts": 3, "mode": "standard"})

        client_kwargs = {"region_name": DYNAMODB_REGION, "config": config}

        # Add endpoint URL for local testing if provided
        if DYNAMODB_ENDPOINT_URL:
            client_kwargs["endpoint_url"] = DYNAMODB_ENDPOINT_URL

        # Use credentials from environment if provided
        if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
            client_kwargs["aws_access_key_id"] = AWS_ACCESS_KEY_ID
            client_kwargs["aws_secret_access_key"] = AWS_SECRET_ACCESS_KEY
            if AWS_SESSION_TOKEN:
                client_kwargs["aws_session_token"] = AWS_SESSION_TOKEN

        _dynamodb_client = boto3.client("dynamodb", **client_kwargs)

    return _dynamodb_client


def get_dynamodb_resource():
    """
    Get or create a DynamoDB resource for higher-level operations.
    """
    global _dynamodb_resource

    if _dynamodb_resource is None:
        resource_kwargs = {"region_name": DYNAMODB_REGION}

        if DYNAMODB_ENDPOINT_URL:
            resource_kwargs["endpoint_url"] = DYNAMODB_ENDPOINT_URL

        if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
            resource_kwargs["aws_access_key_id"] = AWS_ACCESS_KEY_ID
            resource_kwargs["aws_secret_access_key"] = AWS_SECRET_ACCESS_KEY
            if AWS_SESSION_TOKEN:
                resource_kwargs["aws_session_token"] = AWS_SESSION_TOKEN

        _dynamodb_resource = boto3.resource("dynamodb", **resource_kwargs)

    return _dynamodb_resource


def get_table_name() -> str:
    """
    Get the DynamoDB table name from configuration.
    """
    return DYNAMODB_TABLE_NAME


def get_table():
    """
    Get the DynamoDB table resource.
    """
    dynamodb = get_dynamodb_resource()
    return dynamodb.Table(DYNAMODB_TABLE_NAME)


def validate_aws_credentials() -> bool:
    """
    Validate that AWS credentials are available.
    Returns True if credentials are present, False otherwise.
    """
    # Check for environment variables
    if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
        return True

    # Check for AWS profile
    try:
        session = boto3.Session()
        credentials = session.get_credentials()
        if credentials and credentials.access_key and credentials.secret_key:
            return True
    except Exception:
        pass

    return False


def get_aws_region() -> str:
    """
    Get the AWS region from environment or default.
    """
    return DYNAMODB_REGION


def create_dynamodb_item(data: dict) -> dict:
    """
    Convert a Python dictionary to DynamoDB item format.
    """
    from decimal import Decimal
    import json

    def _convert_value(value):
        if isinstance(value, str):
            return {"S": value}
        elif isinstance(value, (int, float)):
            # Use Decimal for numeric values to avoid floating point issues
            return {"N": str(Decimal(str(value)))}
        elif isinstance(value, bool):
            return {"BOOL": value}
        elif isinstance(value, dict):
            return {"M": {k: _convert_value(v) for k, v in value.items()}}
        elif isinstance(value, list):
            return {"L": [_convert_value(v) for v in value]}
        elif value is None:
            return {"NULL": True}
        else:
            # Try to serialize as JSON string
            try:
                return {"S": json.dumps(value)}
            except:
                return {"S": str(value)}

    return {k: _convert_value(v) for k, v in data.items()}


def parse_dynamodb_item(item: dict) -> dict:
    """
    Convert a DynamoDB item to Python dictionary.
    """
    import json
    from decimal import Decimal

    def _convert_value(value_dict):
        if "S" in value_dict:
            # Try to parse JSON strings
            try:
                return json.loads(value_dict["S"])
            except json.JSONDecodeError:
                return value_dict["S"]
        elif "N" in value_dict:
            # Convert Decimal to float or int
            num_str = value_dict["N"]
            try:
                if "." in num_str:
                    return float(num_str)
                else:
                    return int(num_str)
            except ValueError:
                return Decimal(num_str)
        elif "BOOL" in value_dict:
            return value_dict["BOOL"]
        elif "M" in value_dict:
            return {k: _convert_value(v) for k, v in value_dict["M"].items()}
        elif "L" in value_dict:
            return [_convert_value(v) for v in value_dict["L"]]
        elif "NULL" in value_dict:
            return None
        else:
            return value_dict

    return {k: _convert_value(v) for k, v in item.items()}
