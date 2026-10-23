import os
import boto3
import cohere
import deepl
import openai
from google.cloud import vision
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()

def get_google_vision_client() -> vision.ImageAnnotatorClient:
    """Initializes and returns a Google Cloud Vision client."""
    return vision.ImageAnnotatorClient()

def get_openai_client() -> openai.OpenAI:
    """Initializes and returns an OpenAI client."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    return openai.OpenAI(api_key=api_key)

def get_aws_textract_client():
    """Initializes and returns an AWS Textract client."""
    return boto3.client(
        "textract",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

def get_aws_rekognition_client():
    """Initializes and returns an AWS Rekognition client."""
    return boto3.client(
        "rekognition",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

def get_cohere_client() -> cohere.Client:
    """Initializes and returns a Cohere client."""
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")
    return cohere.Client(api_key)

def get_deepl_translator() -> deepl.Translator:
    """Initializes and returns a DeepL Translator client."""
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")
    return deepl.Translator(auth_key)

def get_azure_blob_service_client() -> BlobServiceClient:
    """Initializes and returns an Azure Blob Service client."""
    connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    if not connect_str:
        raise ValueError("AZURE_STORAGE_CONNECTION_STRING environment variable not set.")
    return BlobServiceClient.from_connection_string(connect_str)
