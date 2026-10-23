import os
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

def dynamodb_item_to_python_obj(item_obj):
    if isinstance(item_obj, dict):
        result = {}
        for k, v in item_obj.items():
            if 'S' in v:
                result[k] = v['S']
            elif 'N' in v:
                try:
                    result[k] = int(v['N'])
                except ValueError:
                    result[k] = float(v['N'])
            elif 'BOOL' in v:
                result[k] = v['BOOL']
            elif 'NULL' in v and v['NULL']:
                result[k] = None
            elif 'M' in v:
                result[k] = dynamodb_item_to_python_obj(v['M'])
            elif 'L' in v:
                result[k] = [dynamodb_item_to_python_obj(elem) for elem in v['L']]
            else:
                result[k] = v
        return result
    elif isinstance(item_obj, list):
        return [dynamodb_item_to_python_obj(elem) for elem in item_obj]
    else:
        return item_obj

def fetch_document(key_name: str, key_value: str):
    dynamodb = get_dynamodb_client()
    table_name = get_dynamodb_table_name()

    response = dynamodb.get_item(
        TableName=table_name,
        Key={
            key_name: {'S': key_value}
        }
    )

    item = response.get('Item')
    if item:
        return dynamodb_item_to_python_obj(item)
    return None
