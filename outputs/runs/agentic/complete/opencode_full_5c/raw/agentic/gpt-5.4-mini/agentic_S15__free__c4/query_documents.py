from typing import Any, Dict

from boto3.dynamodb.conditions import Attr, Key
from botocore.exceptions import ClientError

from database_client import get_dynamodb_table
from database_models import response_payload


def query_documents(
    field_name: str, field_value: Any, partition_key: str = None
) -> Dict[str, Any]:
    table = get_dynamodb_table()
    try:
        if partition_key is not None:
            result = table.query(
                KeyConditionExpression=Key("partition_key").eq(partition_key)
                & Key(field_name).eq(field_value)
            )
        else:
            result = table.scan(FilterExpression=Attr(field_name).eq(field_value))
        return response_payload(True, data={"items": result.get("Items", [])})
    except ClientError as exc:
        return response_payload(False, error=str(exc))


def handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    return query_documents(
        event["field_name"], event["field_value"], event.get("partition_key")
    )
