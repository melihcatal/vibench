import os
import datetime
from typing import Dict, Any, Optional
import boto3

def get_boto3_resource(service_name: str, region_name: Optional[str] = None):
    if region_name is None:
        region_name = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.resource(service_name, region_name=region_name)

def get_env_variable(var_name: str, default_value: Optional[str] = None) -> str:
    value = os.environ.get(var_name, default_value)
    if value is None:
        raise ValueError(f"Environment variable '{var_name}' is not set.")
    return value

def record_message_summary(
    summary_data: Dict[str, Any],
    table_name: Optional[str] = None
) -> Dict[str, Any]:
    if table_name is None:
        table_name = get_env_variable("DYNAMODB_SUMMARY_TABLE")

    dynamodb = get_boto3_resource("dynamodb")
    table = dynamodb.Table(table_name)

    if 'timestamp' not in summary_data:
        summary_data['timestamp'] = datetime.datetime.now(datetime.timezone.utc).isoformat()

    if 'SummaryKey' not in summary_data:
        summary_data['SummaryKey'] = 'global_message_processing_summary'

    response = table.put_item(
        Item=summary_data
    )
    return response
