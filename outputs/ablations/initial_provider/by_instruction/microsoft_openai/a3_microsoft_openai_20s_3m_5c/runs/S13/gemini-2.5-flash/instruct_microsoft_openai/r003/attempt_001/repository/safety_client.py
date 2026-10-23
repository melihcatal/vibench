import openai
import os
import boto3
import vertexai
from vertexai.generative_models import GenerativeModel
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from google.cloud import translate_v3 as translation
import cohere
from google.cloud import texttospeech

def get_openai_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    return openai.OpenAI(api_key=api_key)

def get_azure_content_safety_client():
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT or AZURE_CONTENT_SAFETY_KEY environment variable not set")
    return ContentSafetyClient(endpoint, AzureKeyCredential(key))

def get_aws_ssm_client():
    # AWS SDK (boto3) automatically uses environment variables like AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION
    # or IAM roles if running on EC2/ECS/EKS.
    return boto3.client('ssm')

def get_gemini_pro_client():
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION")
    if not project_id or not location:
        raise ValueError("GOOGLE_CLOUD_PROJECT or GOOGLE_CLOUD_LOCATION environment variable not set")
    vertexai.init(project=project_id, location=location)
    return GenerativeModel("gemini-pro")

def get_google_translate_client():
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set")
    return translation.TranslationServiceClient()

def get_cohere_client():
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set")
    return cohere.Client(api_key=api_key)

def get_google_text_to_speech_client():
    return texttospeech.TextToSpeechClient()
