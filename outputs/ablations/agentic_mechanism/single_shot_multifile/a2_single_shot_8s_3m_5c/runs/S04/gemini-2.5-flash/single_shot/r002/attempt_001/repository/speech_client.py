import boto3
import os
from openai import OpenAI
from azure.cognitiveservices.contentmoderator import ContentModeratorClient
from msrest.authentication import CognitiveServicesCredentials

def get_aws_transcribe_client():
    return boto3.client("transcribe", region_name=os.getenv("AWS_REGION", "us-east-1"))

def get_aws_translate_client():
    return boto3.client("translate", region_name=os.getenv("AWS_REGION", "us-east-1"))

def get_openai_client():
    return OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )

def get_azure_content_moderator_client():
    key = os.getenv("AZURE_MODERATOR_KEY")
    endpoint = os.getenv("AZURE_MODERATOR_ENDPOINT")
    if not key or not endpoint:
        raise ValueError("AZURE_MODERATOR_KEY and AZURE_MODERATOR_ENDPOINT must be set in environment variables.")
    return ContentModeratorClient(
        endpoint=endpoint,
        credentials=CognitiveServicesCredentials(key)
    )
