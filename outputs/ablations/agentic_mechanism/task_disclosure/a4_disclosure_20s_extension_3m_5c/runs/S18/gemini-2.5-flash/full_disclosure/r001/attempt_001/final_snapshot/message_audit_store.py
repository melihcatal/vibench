import boto3
import os
import datetime
import json

class MessageAuditStore:
    def __init__(self):
        self.dynamodb = boto3.client('dynamodb')
        self.table_name = os.environ.get('MESSAGE_AUDIT_TABLE_NAME', 'MessageAuditRecords')

    def save_record(self, message_id: str, record_data: dict):
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        item = {
            'message_id': {'S': message_id},
            'timestamp': {'S': timestamp},
            'record_data': {'S': json.dumps(record_data)}
        }
        self.dynamodb.put_item(
            TableName=self.table_name,
            Item=item
        )

    def get_record(self, message_id: str):
        response = self.dynamodb.get_item(
            TableName=self.table_name,
            Key={
                'message_id': {'S': message_id}
            }
        )
        item = response.get('Item')
        if item:
            return {
                'message_id': item['message_id']['S'],
                'timestamp': item['timestamp']['S'],
                'record_data': json.loads(item['record_data']['S'])
            }
        return None
