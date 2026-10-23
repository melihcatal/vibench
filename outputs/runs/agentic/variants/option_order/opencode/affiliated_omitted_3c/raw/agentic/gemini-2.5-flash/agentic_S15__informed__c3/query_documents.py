import os
from database_client import get_dynamodb_resource
from boto3.dynamodb.conditions import Key
from typing import Dict, Any, List


def query_documents(
    table_name: str, key_condition_expression: Any, filter_expression: Any = None
) -> List[Dict[str, Any]]:
    dynamodb = get_dynamodb_resource()
    table = dynamodb.Table(table_name)

    query_params = {"KeyConditionExpression": key_condition_expression}
    if filter_expression:
        query_params["FilterExpression"] = filter_expression

    response = table.query(**query_params)
    return response.get("Items", [])
