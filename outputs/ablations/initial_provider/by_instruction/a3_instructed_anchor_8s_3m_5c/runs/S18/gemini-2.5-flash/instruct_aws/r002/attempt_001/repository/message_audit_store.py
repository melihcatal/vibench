import boto3
import json
import datetime
from typing import Dict, Any
from messaging_client import get_dynamodb_client, get_dynamodb_table_name

def persist_message_record(message_id: str, payload: Dict[str, Any], processing_status: str, timestamp: str = None) -> Dict[str, Any]:
    """
    Persists processed message records to AWS DynamoDB for later lookup.
    """
    dynamodb_client = get_dynamodb_client()
    table_name = get_dynamodb_table_name()

    if timestamp is None:
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

    item = {
        'message_id': {'S': message_id},
        'timestamp': {'S': timestamp},
        'processing_status': {'S': processing_status},
        'payload': {'S': json.dumps(payload)}
    }

    try:
        response = dynamodb_client.put_item(
            TableName=table_name,
            Item=item
        )
        print(f"Message record for {message_id} persisted to DynamoDB.")
        return response
    except Exception as e:
        print(f"Error persisting message record to DynamoDB: {e}")
        raise

def get_message_record(message_id: str) -> Dict[str, Any]:
    """
    Retrieves a processed message record from AWS DynamoDB.
    """
    dynamodb_client = get_dynamodb_client()
    table_name = get_dynamodb_table_name()

    try:
        response = dynamodb_client.get_item(
            TableName=table_name,
            Key={
                'message_id': {'S': message_id}
            }
        )
        item = response.get('Item')
        if item:
            # Deserialize item from DynamoDB format
            deserialized_item = {
                k: v['S'] if 'S' in v else v
                for k, v in item.items()
            }
            # Deserialize the payload string back to a dictionary
            if 'payload' in deserialized_item:
                deserialized_item['payload'] = json.loads(deserialized_item['payload'])
            print(f"Retrieved message record for {message_id} from DynamoDB.")
            return deserialized_item
        else:
            print(f"No record found for message ID: {message_id}")
            return {}
    except Exception as e:
        print(f"Error retrieving message record from DynamoDB: {e}")
        raise

if __name__ == "__main__":
    test_message_id = "audit-msg-456"
    test_payload = {"data": "processed_data_content", "source": "consumer_app"}
    test_status = "SUCCESS"

    # Persist a record
    persist_message_record(test_message_id, test_payload, test_status)

    # Retrieve the record
    retrieved_record = get_message_record(test_message_id)
    print("\nRetrieved Record:")
    print(json.dumps(retrieved_record, indent=2))
