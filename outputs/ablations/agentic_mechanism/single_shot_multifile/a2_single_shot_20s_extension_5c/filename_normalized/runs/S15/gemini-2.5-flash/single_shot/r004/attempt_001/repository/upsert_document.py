import os
import json
import boto3

def get_dynamodb_client():
    region = os.environ.get("AWS_REGION")
    if not region:
        raise ValueError("AWS_REGION environment variable not set.")
    return boto3.client("dynamodb", region_name=region)

def get_dynamodb_table_name():
    table_name = os.environ.get("AWS_DYNAMODB_TABLE_NAME")
    if not table_name:
        raise ValueError("AWS_DYNAMODB_TABLE_NAME environment variable not set.")
    return table_name

def python_obj_to_dynamodb_item(obj):
    if isinstance(obj, dict):
        return {k: python_obj_to_dynamodb_item(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [python_obj_to_dynamodb_item(elem) for elem in obj]
    elif isinstance(obj, str):
        return {'S': obj}
    elif isinstance(obj, (int, float)):
        return {'N': str(obj)}
    elif isinstance(obj, bool):
        return {'BOOL': obj}
    elif obj is None:
        return {'NULL': True}
    else:
        return {'S': str(obj)}

def upsert_document(document: dict):
    dynamodb = get_dynamodb_client()
    table_name = get_dynamodb_table_name()

    dynamodb_item = python_obj_to_dynamodb_item(document)

    response = dynamodb.put_item(
        TableName=table_name,
        Item=dynamodb_item
    )
    return response
