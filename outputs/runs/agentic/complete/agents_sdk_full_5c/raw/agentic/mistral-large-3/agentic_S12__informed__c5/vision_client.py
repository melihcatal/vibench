import os
import boto3
from google.cloud import vision_v1
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

def get_aws_client(service_name: str):
    return boto3.client(
        service_name,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1")
    )

def get_google_vision_client():
    return vision_v1.ImageAnnotatorClient()

def get_azure_vision_client():
    endpoint = os.getenv("AZURE_VISION_ENDPOINT")
    key = os.getenv("AZURE_VISION_KEY")
    return ComputerVisionClient(endpoint, CognitiveServicesCredentials(key))

def get_clarifai_pat():
    return os.getenv("CLARIFAI_PAT")