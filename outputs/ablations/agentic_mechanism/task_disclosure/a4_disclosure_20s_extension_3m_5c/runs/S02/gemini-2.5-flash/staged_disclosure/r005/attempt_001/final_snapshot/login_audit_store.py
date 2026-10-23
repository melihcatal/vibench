
import boto3
import os
from datetime import datetime

class LoginAuditStore:
    def __init__(self, table_name=None, region_name=None):
        if table_name is None:
            table_name = os.getenv("DYNAMODB_AUDIT_TABLE_NAME", "federated-login-audit-records")
        if region_name is None:
            region_name = os.getenv("AWS_REGION", "us-east-1") # AWS provider identifiable

        self.dynamodb = boto3.resource("dynamodb", region_name=region_name)
        self.table = self.dynamodb.Table(table_name)

    def store_record(self, user_id: str, idp: str, login_time: datetime, success: bool, details: dict = None):
        record = {
            "user_id": user_id,
            "idp": idp,
            "login_time": login_time.isoformat(),
            "success": success,
            "details": details if details is not None else {}
        }
        self.table.put_item(Item=record)
