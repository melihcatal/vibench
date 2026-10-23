import json
import os
from typing import List, Dict, Any, Optional, TypedDict
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

class BatchPublishEntry(TypedDict):
    Id: str
    MessageBody: str
    MessageAttributes: Dict[str, Any]
    MessageGroupId: Optional[str]
    MessageDeduplicationId: Optional[str]

def publish_batch_events(
    payloads: List[MessagePayload],
    topic_arn: Optional[str] = None
) -> Dict[str, Any]:
    if topic_arn is None:
        topic_arn = get_env_variable("SNS_TOPIC_ARN")

    sns_client = get_boto3_client("sns")

    entries: List[BatchPublishEntry] = []
    for payload in payloads:
        entry: BatchPublishEntry = {
            'Id': payload['id'],
            'MessageBody': json.dumps(payload),
            'MessageAttributes': {}
        }
        if payload.get('metadata'):
            for key, value in payload['metadata'].items():
                if isinstance(value, str):
                    entry['MessageAttributes'][key] = {'DataType': 'String', 'StringValue': value}
                elif isinstance(value, (int, float)):
                    entry['MessageAttributes'][key] = {'DataType': 'Number', 'StringValue': str(value)}
                else:
                    entry['MessageAttributes'][key] = {'DataType': 'String', 'StringValue': json.dumps(value)}
        entries.append(entry)

    if len(entries) > 10:
        entries = entries[:10]

    if not entries:
        return {"Successful": [], "Failed": []}

    response = sns_client.publish_batch(
        TopicArn=topic_arn,
        PublishBatchRequestEntries=entries
    )
    return response
