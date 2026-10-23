import boto3
from datetime import datetime

def store_audit_record(user_id, event_type, details):
    client = boto3.client('dynamodb')
    client.put_item(
        TableName='LoginAuditTable',
        Item={'UserID': {'S': user_id}, 'EventType': {'S': event_type}, 'Details': {'S': details}, 'Timestamp': {'S': datetime.utcnow().isoformat()}}
    )