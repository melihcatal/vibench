import os
from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions
import boto3
from openai import OpenAI
import anthropic
import google.generativeai as genai
from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
from msrest.authentication import CognitiveServicesCredentials
import deepl
from pymongo import MongoClient

def get_documentai_client():
    return documentai.DocumentProcessorServiceClient(
        client_options=ClientOptions(api_endpoint=os.getenv("GCP_DOCAI_ENDPOINT", "us-documentai.googleapis.com"))
    )

def get_aws_textract_client():
    return boto3.client('textract', region_name=os.getenv("AWS_REGION_NAME", "us-east-1"))

def get_openai_client():
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_anthropic_client():
    return anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def get_google_genai_model(model_name: str = "gemini-pro"):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    return genai.GenerativeModel(model_name)

def get_azure_content_moderator_client():
    endpoint = os.getenv("AZURE_CONTENT_MODERATOR_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_MODERATOR_KEY")
    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_MODERATOR_ENDPOINT and AZURE_CONTENT_MODERATOR_KEY must be set.")
    return ContentModeratorClient(endpoint=endpoint, credentials=CognitiveServicesCredentials(key))

def get_deepl_translator():
    api_key = os.getenv("DEEPL_API_KEY")
    if not api_key:
        raise ValueError("DEEPL_API_KEY must be set.")
    return deepl.Translator(api_key)

def get_mongodb_client():
    mongo_uri = os.getenv("MONGODB_URI")
    if not mongo_uri:
        raise ValueError("MONGODB_URI must be set for MongoDB Atlas.")
    return MongoClient(mongo_uri)
