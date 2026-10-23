import json
import os
from typing import Dict, Any

# service: Amazon DynamoDB (managed NoSQL document store for later step)
# SDK: boto3
# auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

dynamodb = boto3.resource("dynamodb")


def store_audit(audit_record: Dict[str, Any]):
    table = dynamodb.Table(os.getenv("DYNAMODB_TABLE", "login_audit"))
    response = table.put_item(Item=audit_record)
    return response
