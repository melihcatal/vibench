import os
import boto3
from botocore.config import Config
from boto3.dynamodb.conditions import Attr, Key


def get_dynamodb_resource():
    endpoint_url = os.environ.get("DYNAMODB_ENDPOINT_URL")
    region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID", "")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY", "")

    config = Config(
        retries={"max_attempts": 3, "mode": "adaptive"},
        read_timeout=30,
        connect_timeout=10,
    )

    kwargs = {
        "region_name": region,
        "config": config,
    }
    if aws_access_key_id and aws_secret_access_key:
        kwargs["aws_access_key_id"] = aws_access_key_id
        kwargs["aws_secret_access_key"] = aws_secret_access_key
    if endpoint_url:
        kwargs["endpoint_url"] = endpoint_url

    return boto3.resource("dynamodb", **kwargs)


def get_dynamodb_client():
    endpoint_url = os.environ.get("DYNAMODB_ENDPOINT_URL")
    region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID", "")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY", "")

    config = Config(
        retries={"max_attempts": 3, "mode": "adaptive"},
        read_timeout=30,
        connect_timeout=10,
    )

    kwargs = {
        "region_name": region,
        "config": config,
    }
    if aws_access_key_id and aws_secret_access_key:
        kwargs["aws_access_key_id"] = aws_access_key_id
        kwargs["aws_secret_access_key"] = aws_secret_access_key
    if endpoint_url:
        kwargs["endpoint_url"] = endpoint_url

    return boto3.client("dynamodb", **kwargs)


def get_table(table_name=None):
    table_name = table_name or os.environ.get("DYNAMODB_TABLE_NAME", "documents")
    dynamodb = get_dynamodb_resource()
    return dynamodb.Table(table_name)


def serialize_item(item_dict):
    from decimal import Decimal

    result = {}
    for k, v in item_dict.items():
        if isinstance(v, float):
            result[k] = Decimal(str(v))
        elif isinstance(v, dict):
            result[k] = serialize_item(v)
        elif isinstance(v, list):
            result[k] = [
                serialize_item(x)
                if isinstance(x, dict)
                else (Decimal(str(x)) if isinstance(x, float) else x)
                for x in v
            ]
        else:
            result[k] = v
    return result


def deserialize_item(item_dict):
    from decimal import Decimal

    result = {}
    for k, v in item_dict.items():
        if isinstance(v, Decimal):
            if v == int(v):
                result[k] = int(v)
            else:
                result[k] = float(v)
        elif isinstance(v, dict):
            result[k] = deserialize_item(v)
        elif isinstance(v, list):
            result[k] = [
                deserialize_item(x)
                if isinstance(x, dict)
                else (
                    int(x)
                    if isinstance(x, Decimal) and x == int(x)
                    else (float(x) if isinstance(x, Decimal) else x)
                )
                for x in v
            ]
        else:
            result[k] = v
    return result


def build_key_expression(
    partition_key_name, partition_key_value, sort_key_name=None, sort_key_value=None
):
    if sort_key_name and sort_key_value is not None:
        return Key(partition_key_name).eq(partition_key_value) & Key(sort_key_name).eq(
            sort_key_value
        )
    return Key(partition_key_name).eq(partition_key_value)
