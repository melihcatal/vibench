import os
import boto3
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
import openai
import cohere

def get_transcribe_client():
    return boto3.client(
        "transcribe",
        region_name=os.environ.get("AWS_REGION"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )

def get_s3_client():
    return boto3.client(
        "s3",
        region_name=os.environ.get("AWS_REGION"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )

def get_translate_client():
    return boto3.client(
        "translate",
        region_name=os.environ.get("AWS_REGION"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )

def get_content_safety_client():
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    return ContentSafetyClient(endpoint, AzureKeyCredential(key))

def get_openai_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    return openai.OpenAI(api_key=api_key)

def get_cohere_client():
    api_key = os.environ.get("COHERE_API_KEY")
    return cohere.Client(api_key=api_key)