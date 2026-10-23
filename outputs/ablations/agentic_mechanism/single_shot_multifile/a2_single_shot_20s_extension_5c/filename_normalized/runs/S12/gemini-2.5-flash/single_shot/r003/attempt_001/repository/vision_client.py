import os
import boto3
from google.cloud import vision_v1, translate_v3
from azure.ai.vision import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from openai import OpenAI

def get_aws_rekognition_client():
    return boto3.client(
        'rekognition',
        region_name=os.environ.get('AWS_REGION'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )

def get_aws_s3_client():
    return boto3.client(
        's3',
        region_name=os.environ.get('AWS_REGION'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )

def get_google_vision_client():
    return vision_v1.ImageAnnotatorClient()

def get_google_translate_client():
    return translate_v3.TranslationServiceClient()

def get_azure_vision_client():
    endpoint = os.environ.get('AZURE_VISION_ENDPOINT')
    key = os.environ.get('AZURE_VISION_KEY')
    return ImageAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def get_azure_content_safety_client():
    endpoint = os.environ.get('AZURE_CONTENT_SAFETY_ENDPOINT')
    key = os.environ.get('AZURE_CONTENT_SAFETY_KEY')
    return ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def get_openai_client():
    api_key = os.environ.get('OPENAI_API_KEY')
    return OpenAI(api_key=api_key)
