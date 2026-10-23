from typing import Any, Dict

import boto3


def create_request(table_name: str, key: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'TableName': table_name,
        'Key': key
    }


def create_response(data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'statusCode': 200,
        'body': data
    }


def normalize_item(item: Dict[str, Any]) -> Dict[str, Any]:
    normalized_item = {}
    for key, value in item.items():
        if isinstance(value, dict):
            normalized_item[key] = normalize_item(value)
        else:
            normalized_item[key] = value
    return normalized_item
