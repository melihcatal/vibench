import os
from mistralai.client import MistralClient
from anthropic import Anthropic
from google.generativeai import GenerativeModel
import boto3

def get_mistral_client():
    return MistralClient(api_key=os.getenv('MISTRAL_API_KEY'))

def get_anthropic_client():
    return Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def get_gemini_model():
    return GenerativeModel('gemini-pro')

def get_bedrock_client():
    return boto3.client('bedrock-runtime', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))