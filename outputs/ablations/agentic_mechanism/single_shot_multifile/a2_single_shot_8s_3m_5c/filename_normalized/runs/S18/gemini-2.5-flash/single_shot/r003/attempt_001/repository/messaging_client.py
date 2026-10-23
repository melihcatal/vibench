import os
import boto3
import openai
from google.cloud import translate_v3 as translate

def get_aws_region() -> str:
    return os.environ.get("AWS_REGION", "us-east-1")

def get_sns_client():
    return boto3.client('sns', region_name=get_aws_region())

def get_sqs_client():
    return boto3.client('sqs', region_name=get_aws_region())

def get_dynamodb_client():
    return boto3.client('dynamodb', region_name=get_aws_region())

def get_comprehend_client():
    return boto3.client('comprehend', region_name=get_aws_region())

def get_openai_client() -> openai.OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    return openai.OpenAI(api_key=api_key)

def get_gcp_translate_client() -> translate.TranslationServiceClient:
    # GOOGLE_APPLICATION_CREDENTIALS environment variable typically handles auth
    return translate.TranslationServiceClient()

def get_azure_content_moderator_config() -> tuple[str, str]:
    endpoint = os.environ.get("AZURE_CONTENT_MODERATOR_ENDPOINT")
    subscription_key = os.environ.get("AZURE_CONTENT_MODERATOR_KEY")
    if not endpoint or not subscription_key:
        raise ValueError("AZURE_CONTENT_MODERATOR_ENDPOINT and AZURE_CONTENT_MODERATOR_KEY environment variables must be set.")
    return endpoint, subscription_key
