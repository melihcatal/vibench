import os
import boto3
from google.cloud import vision
from google.cloud import translate_v2 as translate
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
import openai
from anthropic import Anthropic
import cohere

def get_vision_client():
    return vision.ImageAnnotatorClient()

def get_textract_client():
    region = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    return boto3.client('textract', region_name=region)

def get_translate_client():
    return translate.Client()

def get_document_intelligence_client():
    endpoint = os.getenv('AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT')
    key = os.getenv('AZURE_DOCUMENT_INTELLIGENCE_KEY')
    if not endpoint or not key:
        raise ValueError('AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and KEY required')
    return DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def get_openai_client():
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError('OPENAI_API_KEY required')
    return openai.OpenAI(api_key=api_key)

def get_anthropic_client():
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError('ANTHROPIC_API_KEY required')
    return Anthropic(api_key=api_key)

def get_cohere_client():
    api_key = os.getenv('COHERE_API_KEY')
    if not api_key:
        raise ValueError('COHERE_API_KEY required')
    return cohere.Client(api_key)