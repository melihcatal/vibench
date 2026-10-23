import os
import boto3
from typing import Any
from azure.core.credentials import AzureKeyCredential
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from google.cloud import vision
from clarifai.client.model import Model

def load_image_bytes(image_path: str) -> bytes:
    with open(image_path, 'rb') as image_file:
        return image_file.read()

def get_google_vision_client() -> vision.ImageAnnotatorClient:
    return vision.ImageAnnotatorClient()

def get_azure_vision_client() -> ImageAnalysisClient:
    endpoint = os.environ['AZURE_VISION_ENDPOINT']
    key = os.environ['AZURE_VISION_KEY']
    return ImageAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def get_rekognition_client() -> Any:
    return boto3.client('rekognition')

def get_clarifai_moderation_model() -> Model:
    pat = os.environ['CLARIFAI_PAT']
    return Model(
        "https://clarifai.com/clarifai/main/models/moderation",
        pat=pat
    )