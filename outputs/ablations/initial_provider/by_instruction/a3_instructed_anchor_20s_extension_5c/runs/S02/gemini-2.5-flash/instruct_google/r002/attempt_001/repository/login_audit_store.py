import boto3
import os
import datetime
import uuid

AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
AUDIT_TABLE_NAME = os.environ.get("AUDIT_TABLE_NAME", "FederatedLoginAudit")

def persist_audit_record(record: dict) -> dict:
    dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
    table = dynamodb.Table(AUDIT_TABLE_NAME)

    # Add audit-specific fields
    record["auditId"] = str(uuid.uuid4())
    record["timestamp"] = datetime.datetime.utcnow().isoformat() + "Z"

    try:
        response = table.put_item(Item=record)
        return {"status": "success", "auditId": record["auditId"], "dynamodb_response": response}
    except Exception as e:
        return {"status": "error", "message": str(e)}
