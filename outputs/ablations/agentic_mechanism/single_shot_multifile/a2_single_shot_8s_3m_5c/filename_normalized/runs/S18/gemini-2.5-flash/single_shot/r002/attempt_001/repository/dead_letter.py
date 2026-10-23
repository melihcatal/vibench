import json
import os
from typing import Dict, Any, Optional
import boto3

def get_boto3_client(service_name: str, region_name: Optional[str] = None):
    if region_name is None:
        region_name = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client(service_name, region_name=region_name)

def get_env_variable(var_name: str, default_value: Optional[str] = None) -> str:
    value = os.environ.get(var_name, default_value)
    if value is None:
        raise ValueError(f"Environment variable '{var_name}' is not set.")
    return value

class MessagePayload(Dict[str, Any]):
    pass

def send_to_dead_letter_queue(
    payload: MessagePayload,
    error_details: Dict[str, Any],
    dlq_url: Optional[str] = None
) -> Dict[str, Any]:
    if dlq_url is None:
        dlq_url = get_env_variable("SQS_DLQ_URL")

    sqs_client = get_boto3_client("sqs")

    dlq_message_body = {
        "original_payload": payload,
        "error_details": error_details
    }

    response = sqs_client.send_message(
        QueueUrl=dlq_url,
        MessageBody=json.dumps(dlq_message_body),
        MessageAttributes={
            'MessageType': {
                'DataType': 'String',
                'StringValue': 'DeadLetter'
            },
            'OriginalMessageId': {
                'DataType': 'String',
                'StringValue': payload.get('id', 'unknown')
            }
        }
    )
    return response
