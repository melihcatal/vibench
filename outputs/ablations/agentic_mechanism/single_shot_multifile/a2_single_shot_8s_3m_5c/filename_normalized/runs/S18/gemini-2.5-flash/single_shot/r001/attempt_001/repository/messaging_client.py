import os
import boto3
from google.cloud import translate_v2 as translate
import openai

def get_sns_client():
    region = os.environ.get('AWS_REGION', 'us-east-1')
    return boto3.client('sns', region_name=region)

def get_sqs_client():
    region = os.environ.get('AWS_REGION', 'us-east-1')
    return boto3.client('sqs', region_name=region)

def get_dynamodb_client():
    region = os.environ.get('AWS_REGION', 'us-east-1')
    return boto3.client('dynamodb', region_name=region)

def get_openai_client():
    return openai.OpenAI()

def get_google_translate_client():
    return translate.Client()