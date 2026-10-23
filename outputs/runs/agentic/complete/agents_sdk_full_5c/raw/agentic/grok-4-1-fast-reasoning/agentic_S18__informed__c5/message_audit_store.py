import os
import boto3
from boto3.dynamodb.conditions import Key
from typing import Dict, Any

TABLE_NAME = os.getenv("AUDIT_TABLE_NAME", "MessageAudits")

def persist_message_record(record: Dict[str, Any]):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(TABLE_NAME)
    table.put_item(Item=record)

def lookup_message_record(event_id: str) -> Dict[str, Any]:
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(TABLE_NAME)
    response = table.query(
        KeyConditionExpression=Key('event_id').eq(event_id)
    )
    if response['Items']:
        return response['Items'][0]
    return {}