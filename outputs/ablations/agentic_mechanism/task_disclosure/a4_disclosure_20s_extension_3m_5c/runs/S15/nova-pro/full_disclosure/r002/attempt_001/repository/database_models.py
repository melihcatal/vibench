from typing import Any, Dict, List

import boto3

dynamodb = boto3.client('dynamodb')


def create_request(table_name: str, item: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'TableName': table_name,
        'Item': item
    }


def create_response(response: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'status': response.get('ResponseMetadata', {}).get('HTTPStatusCode', 500),
        'data': response.get('Attributes', {})
    }


def normalize_item(item: Dict[str, Any]) -> Dict[str, Any]:
    normalized_item = {}
    for key, value in item.items():
        if isinstance(value, list):
            normalized_item[key] = [normalize_item(v) if isinstance(v, dict) else v for v in value]
        elif isinstance(value, dict):
            normalized_item[key] = normalize_item(value)
        else:
            normalized_item[key] = value
    return normalized_item
