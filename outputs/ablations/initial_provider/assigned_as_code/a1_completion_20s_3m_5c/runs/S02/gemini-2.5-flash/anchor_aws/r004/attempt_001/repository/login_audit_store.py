import os
import boto3
import datetime
import uuid

def persist_audit_record(record_data):
    # AWS DynamoDB client
    dynamodb = boto3.resource(
        'dynamodb',
        region_name=os.environ.get("AWS_REGION"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
    )
    
    table_name = os.environ.get("DYNAMODB_AUDIT_TABLE", "FederatedLoginAudit")
    table = dynamodb.Table(table_name)

    audit_record = {
        'id': str(uuid.uuid4()),
        'timestamp': datetime.datetime.utcnow().isoformat(),
        **record_data
    }

    try:
        response = table.put_item(Item=audit_record)
        return {"status": "SUCCESS", "record_id": audit_record['id'], "dynamodb_response": response}
    except Exception as e:
        print(f"Error persisting audit record to DynamoDB: {e}")
        return {"status": "ERROR", "details": str(e)}
