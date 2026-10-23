import os
from typing import Any, Dict


def load_config() -> Dict[str, str]:
    return {
        "aws_region": os.getenv("AWS_REGION", "us-east-1"),
        "sns_topic_arn": os.getenv("SNS_TOPIC_ARN", ""),
        "sqs_queue_url": os.getenv("SQS_QUEUE_URL", ""),
        "dynamodb_table": os.getenv("DYNAMODB_TABLE", "message_audit"),
        "openai_model": os.getenv("OPENAI_MODEL", "gpt-5.4-mini"),
        "azure_content_safety_endpoint": os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT", ""),
        "azure_content_safety_key": os.getenv("AZURE_CONTENT_SAFETY_KEY", ""),
        "azure_translator_key": os.getenv("AZURE_TRANSLATOR_KEY", ""),
        "azure_translator_region": os.getenv("AZURE_TRANSLATOR_REGION", ""),
    }


def aws_client(service: str, region: str = None) -> Any:
    import boto3

    cfg = load_config()
    return boto3.client(service, region_name=region or cfg["aws_region"])


def openai_client() -> Any:
    from openai import OpenAI

    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
