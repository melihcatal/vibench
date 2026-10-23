import os
import boto3
import datetime
import uuid

class LoginAuditStore:
    def __init__(self):
        # AWS DynamoDB client
        self.dynamodb = boto3.resource(
            'dynamodb',
            region_name=os.environ.get("AWS_REGION", "us-east-1"),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
        )
        self.table_name = os.environ.get("DYNAMODB_AUDIT_TABLE", "federated-login-audit")
        self.table = self.dynamodb.Table(self.table_name)

    def save_audit_record(self, event_type: str, user_id: str, details: dict):
        timestamp = datetime.datetime.utcnow().isoformat() + "Z"
        record_id = str(uuid.uuid4())

        item = {
            'record_id': record_id,
            'timestamp': timestamp,
            'event_type': event_type,
            'user_id': user_id,
            'details': details
        }
        self.table.put_item(Item=item)
