import boto3
from botocore.exceptions import ClientError
from identity_client import identity_client
from identity_models import AuditEvent
import json
from decimal import Decimal


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super(DecimalEncoder, self).default(obj)


def store_audit_event(event: AuditEvent):
    """
    Persists a federated login audit event to Amazon DynamoDB.
    """
    dynamodb = boto3.resource(
        "dynamodb",
        aws_access_key_id=identity_client.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=identity_client.AWS_SECRET_ACCESS_KEY,
        region_name=identity_client.AWS_REGION_NAME,
    )
    table = dynamodb.Table(identity_client.DYNAMODB_TABLE_NAME)

    try:
        item_to_store = {
            "event_id": event.event_id,
            "user_id": event.user_id,
            "event_type": event.event_type,
            "timestamp": event.timestamp,
            "details": json.loads(json.dumps(event.details), parse_float=Decimal),
        }

        table.put_item(Item=item_to_store)
        return True
    except ClientError as e:
        print(
            f"Error storing audit event in DynamoDB: {e.response['Error']['Message']}"
        )
        return False
