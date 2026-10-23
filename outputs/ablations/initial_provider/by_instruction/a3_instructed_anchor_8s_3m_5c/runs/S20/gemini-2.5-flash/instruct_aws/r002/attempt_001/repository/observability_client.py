import boto3
import os

def get_cloudwatch_logs_client():
    """Initializes and returns an AWS CloudWatch Logs client."""
    return boto3.client("logs", region_name=os.environ.get("AWS_REGION", "us-east-1"))

def get_cloudwatch_comprehend_client():
    """Initializes and returns an AWS Comprehend client."""
    return boto3.client("comprehend", region_name=os.environ.get("AWS_REGION", "us-east-1"))

def get_cloudwatch_translate_client():
    """Initializes and returns an AWS Translate client."""
    return boto3.client("translate", region_name=os.environ.get("AWS_REGION", "us-east-1"))

def get_anthropic_client():
    """Initializes and returns an Anthropic client."""
    from anthropic import Anthropic
    return Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def get_openai_client():
    """Initializes and returns an OpenAI client."""
    from openai import OpenAI
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
