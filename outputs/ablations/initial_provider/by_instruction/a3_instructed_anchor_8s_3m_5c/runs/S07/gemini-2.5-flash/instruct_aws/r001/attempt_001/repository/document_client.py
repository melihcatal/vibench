import boto3
import os
from google.cloud import language_v1
import openai

def get_textract_client():
    return boto3.client('textract', region_name=os.environ.get('AWS_REGION', 'us-east-1'))

def get_translate_client():
    return boto3.client('translate', region_name=os.environ.get('AWS_REGION', 'us-east-1'))

def get_comprehend_client():
    return boto3.client('comprehend', region_name=os.environ.get('AWS_REGION', 'us-east-1'))

def get_google_nl_client():
    # Google Cloud Natural Language API client
    # Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set or credentials are otherwise available
    return language_v1.LanguageServiceClient()

def get_openai_client():
    # OpenAI client
    # Assumes OPENAI_API_KEY environment variable is set
    return openai.OpenAI()
