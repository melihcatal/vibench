import json
import os

from boto3.dynamodb.conditions import Attr, Key

from database_client import get_partition_key_name, get_table
from database_models import response_payload


def query_documents(value, field_name=None, table_name=None):
    table = get_table(table_name)
    if field_name == get_partition_key_name() or field_name is None:
        key_name = field_name or get_partition_key_name()
        result = table.query(KeyConditionExpression=Key(key_name).eq(value))
    else:
        result = table.scan(FilterExpression=Attr(field_name).eq(value))
    return response_payload(ok=True, documents=result.get("Items", []))


if __name__ == "__main__":
    print(
        json.dumps(
            query_documents(
                os.environ.get("QUERY_VALUE", ""), os.environ.get("QUERY_FIELD")
            )
        )
    )
