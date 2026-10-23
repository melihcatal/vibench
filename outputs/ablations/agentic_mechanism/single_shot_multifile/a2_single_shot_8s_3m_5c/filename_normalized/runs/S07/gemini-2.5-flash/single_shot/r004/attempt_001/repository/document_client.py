import os
from google.cloud import vision_v1, documentai_v1
import boto3
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
import deepl
import openai
import anthropic
import cohere

def get_google_vision_client():
    return vision_v1.ImageAnnotatorClient()

def get_azure_document_intelligence_client():
    endpoint = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY")
    if not endpoint or not key:
        raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY must be set.")
    return DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def get_aws_textract_client():
    return boto3.client('textract', region_name=os.environ.get("AWS_REGION", "us-east-1"))

def get_google_document_ai_client():
    return documentai_v1.DocumentProcessorServiceClient()

def get_deepl_translator():
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY must be set.")
    return deepl.Translator(auth_key)

def get_openai_client():
    return openai.OpenAI()

def get_anthropic_client():
    return anthropic.Anthropic()

def get_cohere_client():
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY must be set.")
    return cohere.Client(api_key)