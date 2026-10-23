import os
import boto3
from mistralai.client import MistralClient
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from openai import OpenAI
import deepl


def get_aws_kms_client():
    return boto3.client(
        "kms",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )


def get_mistral_client():
    return MistralClient(api_key=os.environ.get("MISTRAL_API_KEY"))


def get_azure_content_safety_client():
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    return ContentSafetyClient(endpoint, AzureKeyCredential(key))


def get_openai_client():
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def get_deepl_translator():
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    return deepl.Translator(auth_key)
