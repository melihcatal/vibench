import os
from dotenv import load_dotenv

from clarifai.client.app import App
from google.cloud import vision
import boto3
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential

load_dotenv()


def get_google_vision_client():
    return vision.ImageAnnotatorClient()


def get_rekognition_client():
    return boto3.client(
        "rekognition",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
    )


def get_azure_vision_client():
    endpoint = os.getenv("AZURE_VISION_ENDPOINT")
    key = os.getenv("AZURE_VISION_KEY")
    if not endpoint or not key:
        raise ValueError(
            "Azure Vision endpoint and key must be set in environment variables."
        )
    return ImageAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))


def get_clarifai_app():
    pat = os.getenv("CLARIFAI_PAT")
    if not pat:
        raise ValueError("Clarifai PAT must be set in environment variables.")
    return App(pat=pat)
