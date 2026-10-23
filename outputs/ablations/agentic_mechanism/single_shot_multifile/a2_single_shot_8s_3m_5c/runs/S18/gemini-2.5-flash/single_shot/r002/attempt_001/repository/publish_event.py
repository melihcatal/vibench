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

def publish_json_event(
    payload: MessagePayload,
    topic_arn: Optional[str] = None,
    message_attributes: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    if topic_arn is None:
        topic_arn = get_env_variable("SNS_TOPIC_ARN")

    sns_client = get_boto3_client("sns")

    message_body = json.dumps(payload)

    sns_attributes = {}
    if message_attributes:
        for key, value in message_attributes.items():
            if isinstance(value, str):
                sns_attributes[key] = {'DataType': 'String', 'StringValue': value}
            elif isinstance(value, (int, float)):
                sns_attributes[key] = {'DataType': 'Number', 'StringValue': str(value)}
            else:
                sns_attributes[key] = {'DataType': 'String', 'StringValue': json.dumps(value)}

    response = sns_client.publish(
        TopicArn=topic_arn,
        Message=message_body,
        MessageAttributes=sns_attributes
    )
    return response
