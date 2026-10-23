import os
import boto3
from botocore.exceptions import ClientError
from messaging_models import ProcessingResult


def store_audit_record(record: ProcessingResult):
    table_name = os.getenv("DYNAMODB_AUDIT_TABLE", "message_audit")

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)

    try:
        response = table.put_item(Item=record)
        print(f"Successfully stored audit record: {record['message_id']}")
        return response
    except ClientError as e:
        print(
            f"Error storing audit record in DynamoDB: {e.response['Error']['Message']}"
        )
        return None
