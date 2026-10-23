import json
import os
from typing import Optional, Dict, Any, List, TypedDict
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

class ConsumedMessage(TypedDict):
    id: str
    receipt_handle: str
    body: Dict[str, Any]
    attributes: Dict[str, Any]

def consume_one_message(
    queue_url: Optional[str] = None,
    wait_time_seconds: int = 10
) -> Optional[ConsumedMessage]:
    if queue_url is None:
        queue_url = get_env_variable("SQS_QUEUE_URL")

    sqs_client = get_boto3_client("sqs")

    response = sqs_client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=wait_time_seconds,
        MessageAttributeNames=['All'],
        AttributeNames=['All']
    )

    messages = response.get('Messages', [])
    if not messages:
        return None

    message = messages[0]
    message_id = message.get('MessageId', 'unknown')
    receipt_handle = message.get('ReceiptHandle', '')
    body_str = message.get('Body', '{}')
    
    try:
        body_json = json.loads(body_str)
    except json.JSONDecodeError:
        body_json = {"raw_body": body_str}

    message_attributes = {}
    if 'MessageAttributes' in message:
        for attr_name, attr_value in message['MessageAttributes'].items():
            if 'StringValue' in attr_value:
                message_attributes[attr_name] = attr_value['StringValue']
            elif 'BinaryValue' in attr_value:
                message_attributes[attr_name] = attr_value['BinaryValue']
            
    if 'TopicArn' in message_attributes and 'Message' in body_json:
        try:
            sns_message = json.loads(body_json['Message'])
            body_json = sns_message
            if 'Subject' in body_json:
                message_attributes['Subject'] = body_json['Subject']
        except (json.JSONDecodeError, TypeError):
            pass

    return ConsumedMessage(
        id=message_id,
        receipt_handle=receipt_handle,
        body=body_json,
        attributes=message_attributes
    )

def delete_message(
    receipt_handle: str,
    queue_url: Optional[str] = None
) -> Dict[str, Any]:
    if queue_url is None:
        queue_url = get_env_variable("SQS_QUEUE_URL")

    sqs_client = get_boto3_client("sqs")
    response = sqs_client.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )
    return response
