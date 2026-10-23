import os
import sys
import boto3
import uuid
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from identity_client import IdentityClient
from identity_models import StoreProfileNoteRequest, StoreProfileNoteResponse


def profile_note_store(
    request: StoreProfileNoteRequest, table_name: str = "ProfileNotes"
) -> StoreProfileNoteResponse:
    identity_client = IdentityClient()
    dynamodb_client = identity_client.get_dynamodb_client()

    note_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()

    item = {
        "user_id": {"S": request.user_id},
        "note_id": {"S": note_id},
        "timestamp": {"S": timestamp},
        "content": {"S": request.content},
        "metadata": {
            "S": json.dumps(request.metadata)
        },  # Store metadata as a JSON string
    }

    try:
        # Ensure the table exists. In a production environment, this would be handled
        # by infrastructure setup, but for a standalone script, we can check/create.
        try:
            dynamodb_client.describe_table(TableName=table_name)
        except dynamodb_client.exceptions.ResourceNotFoundException:
            print(f"DynamoDB table {table_name} not found. Creating it...")
            dynamodb_client.create_table(
                TableName=table_name,
                KeySchema=[
                    {"AttributeName": "user_id", "KeyType": "HASH"},  # Partition key
                    {"AttributeName": "note_id", "KeyType": "RANGE"},  # Sort key
                ],
                AttributeDefinitions=[
                    {"AttributeName": "user_id", "AttributeType": "S"},
                    {"AttributeName": "note_id", "AttributeType": "S"},
                ],
                ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
            )
            # Wait until the table exists. This is important for immediate use.
            waiter = dynamodb_client.get_waiter("table_exists")
            waiter.wait(TableName=table_name)
            print(f"Table {table_name} created successfully.")

        dynamodb_client.put_item(TableName=table_name, Item=item)
        return StoreProfileNoteResponse(
            note_id=note_id, message="Profile note stored successfully."
        )
    except Exception as e:
        return StoreProfileNoteResponse(
            note_id="", message=f"Failed to store profile note: {str(e)}"
        )
