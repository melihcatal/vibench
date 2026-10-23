import os
from google.cloud import vision_v1p4, translate_v3
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential
import boto3
import openai

def get_google_vision_client():
    return vision_v1p4.ImageAnnotatorClient()

def get_azure_vision_client():
    endpoint = os.environ.get("AZURE_VISION_ENDPOINT")
    key = os.environ.get("AZURE_VISION_KEY")
    if not endpoint or not key:
        raise ValueError("AZURE_VISION_ENDPOINT and AZURE_VISION_KEY must be set for Azure Vision.")
    return ImageAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def get_aws_rekognition_client():
    return boto3.client("rekognition", region_name=os.environ.get("AWS_REGION", "us-east-1"))

def get_openai_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY must be set for OpenAI.")
    return openai.OpenAI(api_key=api_key)

def get_google_translation_client():
    return translate_v3.TranslationServiceClient()

def get_aws_s3_client():
    return boto3.client("s3", region_name=os.environ.get("AWS_REGION", "us-east-1"))