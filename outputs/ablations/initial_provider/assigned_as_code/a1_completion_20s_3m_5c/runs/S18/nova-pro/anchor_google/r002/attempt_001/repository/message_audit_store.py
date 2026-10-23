import boto3
import json


def persist_message_record(record: Dict[str, Any], table_name: str):
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table(table_name)
    table.put_item(Item=record)