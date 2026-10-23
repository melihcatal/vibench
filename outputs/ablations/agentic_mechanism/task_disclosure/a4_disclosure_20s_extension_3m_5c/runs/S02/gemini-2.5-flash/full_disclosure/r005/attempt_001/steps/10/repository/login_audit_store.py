import os
import boto3

class LoginAuditStore:
    def __init__(self, region_name=None, table_name=None):
        if region_name is None:
            region_name = os.getenv("AWS_REGION", "us-east-1") # AWS provider identification
        if table_name is None:
            self.table_name = os.getenv("AUDIT_TABLE_NAME", "federated-login-audit-records")
        else:
            self.table_name = table_name

        self.dynamodb = boto3.resource("dynamodb", region_name=region_name)
        self.table = self.dynamodb.Table(self.table_name)

    def store_audit_record(self, record: dict):
        # Ensure the record has a unique identifier, e.g., 'event_id'
        if "event_id" not in record:
            raise ValueError("Audit record must contain an 'event_id'.")
        
        # Put item into DynamoDB table
        self.table.put_item(Item=record)
