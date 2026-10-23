import os
import boto3
from botocore.exceptions import ClientError

class LoginAuditStore:
    def __init__(self):
        self.region_name = os.environ.get("AWS_REGION", "us-east-1")
        self.table_name = os.environ.get("DYNAMODB_AUDIT_TABLE", "FederatedLoginAuditRecords")
        self.dynamodb = boto3.resource("dynamodb", region_name=self.region_name)
        self.table = self.dynamodb.Table(self.table_name)

    def persist_audit_record(self, record: dict):
        try:
            response = self.table.put_item(Item=record)
            return response
        except ClientError as e:
            print(f"Error persisting audit record: {e.response['Error']['Message']}")
            raise
