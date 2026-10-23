import os
from typing import Dict, Any
from database_client import get_dynamodb_client
from database_models import Document
import json


def conditional_update(
    table_name: str,
    document_id: str,
    new_content: Dict[str, Any],
    expected_version: int,
) -> Dict[str, Any]:
    dynamodb = get_dynamodb_client()

    response = dynamodb.update_item(
        TableName=table_name,
        Key={"id": {"S": document_id}},
        UpdateExpression="SET content = :new_content, version = :new_version",
        ConditionExpression="version = :expected_version",
        ExpressionAttributeValues={
            ":new_content": {"S": json.dumps(new_content)},
            ":new_version": {"N": str(expected_version + 1)},
            ":expected_version": {"N": str(expected_version)},
        },
        ReturnValues="ALL_NEW",
    )
    return response
