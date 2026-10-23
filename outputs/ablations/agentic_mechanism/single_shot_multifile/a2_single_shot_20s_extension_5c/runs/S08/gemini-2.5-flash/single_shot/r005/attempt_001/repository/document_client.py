import os
import boto3
from google.cloud import documentai_v1beta3 as documentai
from google.cloud import translate_v3 as translate
import openai
import anthropic
import cohere

def get_textract_client():
    return boto3.client(
        'textract',
        region_name=os.environ.get('AWS_REGION', 'us-east-1'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )

def get_documentai_client():
    return documentai.DocumentProcessorServiceClient()

def get_openai_client():
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    return openai.OpenAI()

def get_anthropic_client():
    anthropic_api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not anthropic_api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set.")
    return anthropic.Anthropic(api_key=anthropic_api_key)

def get_cohere_client():
    cohere_api_key = os.environ.get('COHERE_API_KEY')
    if not cohere_api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")
    return cohere.Client(cohere_api_key)

def get_translate_client():
    return translate.TranslationServiceClient()

def get_dynamodb_client():
    return boto3.resource(
        'dynamodb',
        region_name=os.environ.get('AWS_REGION', 'us-east-1'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )
