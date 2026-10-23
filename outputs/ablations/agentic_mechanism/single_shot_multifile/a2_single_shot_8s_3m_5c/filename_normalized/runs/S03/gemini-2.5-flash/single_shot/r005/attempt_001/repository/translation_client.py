import os
import boto3
from google.cloud import translate_v3
from google.cloud import texttospeech_v1
from openai import OpenAI
import cohere

def get_google_translate_client():
    return translate_v3.TranslationServiceClient()

def get_amazon_translate_client():
    region_name = os.getenv('AWS_REGION', 'us-east-1')
    return boto3.client('translate', region_name=region_name)

def get_openai_client():
    return OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_cohere_client():
    return cohere.Client(api_key=os.getenv('COHERE_API_KEY'))

def get_google_tts_client():
    return texttospeech_v1.TextToSpeechClient()
