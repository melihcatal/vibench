import boto3
from typing import Dict, Any

def get_sns_client(region_name: str):
    return boto3.client("sns", region_name=region_name)

def get_sqs_client(region_name: str):
    return boto3.client("sqs", region_name=region_name)

def create_sns_message_attributes(attributes: Dict[str, Any]):
    sns_attributes = {}
    for key, value in attributes.items():
        if isinstance(value, str):
            sns_attributes[key] = {'DataType': 'String', 'StringValue': value}
        elif isinstance(value, (int, float)):
            sns_attributes[key] = {'DataType': 'Number', 'StringValue': str(value)}
        # Add more types if needed, or handle complex objects by serializing to JSON string
    return sns_attributes
