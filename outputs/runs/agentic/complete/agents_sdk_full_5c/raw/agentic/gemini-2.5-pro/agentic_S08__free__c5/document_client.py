# document_client.py
import os
import boto3
import deepl
import anthropic
import openai
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from google.cloud import documentai
from googleapiclient import discovery
from pymongo import MongoClient

def get_azure_document_intelligence_client():
    """Returns an Azure Document Intelligence client."""
    endpoint = os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"]
    key = os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]
    return DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def get_google_document_ai_client():
    """Returns a Google Document AI client."""
    # The client library will automatically find the credentials
    # if you have authenticated with the gcloud CLI.
    # e.g., gcloud auth application-default login
    opts = {"api_endpoint": f"us-documentai.googleapis.com"}
    return documentai.DocumentProcessorServiceClient(client_options=opts)

def get_anthropic_client():
    """Returns an Anthropic client."""
    return anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

def get_bedrock_client():
    """Returns a Boto3 client for Amazon Bedrock."""
    return boto3.client(service_name='bedrock-runtime', region_name='us-east-1')

def get_openai_client():
    """Returns an OpenAI client."""
    return openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_perspective_client():
    """Returns a Google Perspective API client."""
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    return discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_discovery=False,
    )

def get_deepl_translator():
    """Returns a DeepL translator client."""
    auth_key = os.environ["DEEPL_AUTH_KEY"]
    return deepl.Translator(auth_key)

def get_mongo_collection():
    """Returns a MongoDB collection object for expense records."""
    connection_string = os.environ["MONGO_ATLAS_CONNECTION_STRING"]
    client = MongoClient(connection_string)
    db = client["expense_db"]
    return db["records"]
