import os
import boto3
from datetime import datetime
import uuid

def persist_audit_record(event_data: dict, table_name: str) -> dict:
    """
    Persists federated-login audit records in an AWS DynamoDB managed document store.
    """
    dynamodb = boto3.resource('dynamodb', region_name=os.environ.get("AWS_REGION"))
    table = dynamodb.Table(table_name)

    try:
        audit_record = {
            'auditId': str(uuid.uuid4()),
            'timestamp': datetime.utcnow().isoformat(),
            'eventType': event_data.get("eventType", "FederatedLoginEvent"),
            'userId': event_data.get("userId"),
            'provider': event_data.get("provider"),
            'details': event_data  # Store all event data as details
        }

        table.put_item(Item=audit_record)

        return {
            "message": "Audit record persisted successfully.",
            "auditId": audit_record['auditId']
        }
    except Exception as e:
        return {"error": str(e)}
