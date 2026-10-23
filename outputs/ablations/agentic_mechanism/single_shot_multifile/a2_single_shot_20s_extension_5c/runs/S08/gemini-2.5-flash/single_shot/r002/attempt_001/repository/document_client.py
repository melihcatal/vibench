import os
import boto3
from openai import OpenAI
import cohere
from google.cloud import documentai_v1beta3 as documentai
from google.cloud import aiplatform
from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
from msrest.authentication import CognitiveServicesCredentials
import pymongo

# --- AWS Clients ---
def get_textract_client():
    aws_region = os.getenv("AWS_REGION", "us-east-1")
    return boto3.client("textract", region_name=aws_region)

def get_aws_translate_client():
    aws_region = os.getenv("AWS_REGION", "us-east-1")
    return boto3.client("translate", region_name=aws_region)

# --- Google Cloud Clients ---
def get_documentai_client():
    return documentai.DocumentProcessorServiceClient()

def get_vertexai_model(model_name: str = "text-bison@001"):
    project_id = os.getenv("GCP_PROJECT_ID")
    location = os.getenv("GCP_LOCATION", "us-central1")
    if not all([project_id, location]):
        raise ValueError("Missing GCP environment variables: GCP_PROJECT_ID, GCP_LOCATION")
    aiplatform.init(project=project_id, location=location)
    from google.cloud.aiplatform.preview.language_models import TextGenerationModel
    return TextGenerationModel.from_pretrained(model_name)

# --- Azure Clients ---
def get_azure_content_moderator_client():
    endpoint = os.getenv("AZURE_CONTENT_MODERATOR_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_MODERATOR_KEY")
    if not all([endpoint, key]):
        raise ValueError("Missing Azure Content Moderator environment variables: AZURE_CONTENT_MODERATOR_ENDPOINT, AZURE_CONTENT_MODERATOR_KEY")
    return ContentModeratorClient(endpoint=endpoint, credentials=CognitiveServicesCredentials(key))

# --- OpenAI Client ---
def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Missing OPENAI_API_KEY environment variable.")
    return OpenAI(api_key=api_key)

# --- Cohere Client ---
def get_cohere_client():
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("Missing COHERE_API_KEY environment variable.")
    return cohere.Client(api_key)

# --- MongoDB Atlas Client ---
def get_mongodb_client():
    mongo_uri = os.getenv("MONGO_CONNECTION_STRING")
    if not mongo_uri:
        raise ValueError("Missing MONGO_CONNECTION_STRING environment variable.")
    return pymongo.MongoClient(mongo_uri)
