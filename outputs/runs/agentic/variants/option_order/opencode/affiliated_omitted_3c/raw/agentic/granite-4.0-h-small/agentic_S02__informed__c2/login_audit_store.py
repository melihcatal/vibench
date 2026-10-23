import identity_client
import boto3
from datetime import datetime


def store_audit_record(event_data: Dict[str, Any]):
    # Persist federated-login audit records in Amazon DynamoDB (managed NoSQL document store)
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(identity_client.get_config("AUDIT_TABLE_NAME"))
    # Ensure eventId is unique per request; generate if missing
    event_id = event_data.get("eventId") or str(uuid.uuid4())
    # Set timestamp to ISO 8601 string
    event_data["timestamp"] = datetime.utcnow().isoformat() + "Z"
    # Write item (insert or overwrite)
    table.put_item(Item={**event_data, "eventId": event_id})
