import os
import boto3

class MessageAuditStore:
    def __init__(self):
        self.dynamodb = boto3.resource(
            'dynamodb',
            region_name=os.environ.get('AWS_REGION', 'us-east-1') # Default to us-east-1 if not set
        )
        self.table_name = os.environ.get('DYNAMODB_AUDIT_TABLE', 'MessageAuditTable')
        self.table = self.dynamodb.Table(self.table_name)

    def save_message_record(self, message_id: str, timestamp: str, content: str, status: str):
        """
        Persists a processed message record to DynamoDB.
        """
        try:
            self.table.put_item(
                Item={
                    'message_id': message_id,
                    'timestamp': timestamp,
                    'content': content,
                    'status': status
                }
            )
            print(f"Message record {message_id} saved successfully to DynamoDB table {self.table_name}")
        except Exception as e:
            print(f"Error saving message record {message_id} to DynamoDB: {e}")

