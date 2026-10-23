import os
import boto3
from google.cloud import vision_v1p3beta1 as vision
from google.cloud import aiplatform
from google.cloud import translate_v3 as translate
from azure.core.credentials import AzureKeyCredential
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.contentsafety import ContentSafetyClient
import openai

def get_aws_rekognition_client():
    return boto3.client(
        'rekognition',
        region_name=os.environ.get('AWS_REGION', 'us-east-1'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )

def get_google_vision_client():
    return vision.ImageAnnotatorClient()

def get_google_vertex_ai_generative_model(model_name: str = 'gemini-pro-vision'):
    project_id = os.environ.get('GOOGLE_CLOUD_PROJECT_ID')
    location = os.environ.get('GOOGLE_CLOUD_LOCATION', 'us-central1')
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")
    aiplatform.init(project=project_id, location=location)
    return aiplatform.GenerativeModel(model_name)

def get_google_translate_client():
    return translate.TranslationServiceClient()

def get_azure_ai_vision_client():
    endpoint = os.environ.get('AZURE_AI_VISION_ENDPOINT')
    key = os.environ.get('AZURE_AI_VISION_KEY')
    if not endpoint or not key:
        raise ValueError("Azure AI Vision endpoint and key must be set as environment variables.")
    return ImageAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def get_azure_content_safety_client():
    endpoint = os.environ.get('AZURE_CONTENT_SAFETY_ENDPOINT')
    key = os.environ.get('AZURE_CONTENT_SAFETY_KEY')
    if not endpoint or not key:
        raise ValueError("Azure Content Safety endpoint and key must be set as environment variables.")
    return ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def get_openai_client():
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    return openai.OpenAI(api_key=api_key)

def get_aws_s3_client():
    return boto3.client(
        's3',
        region_name=os.environ.get('AWS_REGION', 'us-east-1'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )