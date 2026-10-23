import os
import boto3
import anthropic
import requests
import deepl


def get_aws_client(service_name: str):
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client(
        service_name,
        region_name=aws_region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )


def get_anthropic_client():
    anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")
    return anthropic.Anthropic(api_key=anthropic_api_key)


def get_azure_content_safety_headers():
    azure_content_safety_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    return {
        "Ocp-Apim-Subscription-Key": azure_content_safety_key,
        "Content-Type": "application/json",
    }


def get_azure_content_safety_endpoint():
    return os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")


def get_deepl_translator():
    deepl_auth_key = os.environ.get("DEEPL_AUTH_KEY")
    return deepl.Translator(deepl_auth_key)
