import json
import datetime
from messaging_client import get_dynamodb_client

def message_audit_store(table_name, message_id, event_type, payload_data, status, config=None):
    config = config or {}
    dynamodb_client = get_dynamodb_client(config.get("region"))

    item = {
        'message_id': {'S': message_id},
        'timestamp': {'S': datetime.datetime.now().isoformat()},
        'event_type': {'S': event_type},
        'payload_data': {'S': json.dumps(payload_data)},
        'status': {'S': status}
    }

    response = dynamodb_client.put_item(
        TableName=table_name,
        Item=item
    )
    return {"status_code": response["ResponseMetadata"]["HTTPStatusCode"]}
