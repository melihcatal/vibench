from identity_client import get_dynamodb_client
import os

def profile_note_store(payload, config=None):
    config = config or {}
    client = get_dynamodb_client()

    table_name = os.environ.get("DYNAMODB_TABLE_NAME")
    user_id = payload["user_id"]
    note_content = payload["note_content"]
    timestamp = payload.get("timestamp") # Optional timestamp

    item = {
        "UserId": {'S': user_id},
        "NoteContent": {'S': note_content},
    }
    if timestamp:
        item["Timestamp"] = {'S': timestamp}

    response = client.put_item(
        TableName=table_name,
        Item=item
    )

    return {"status": "success", "response_metadata": response["ResponseMetadata"]}
