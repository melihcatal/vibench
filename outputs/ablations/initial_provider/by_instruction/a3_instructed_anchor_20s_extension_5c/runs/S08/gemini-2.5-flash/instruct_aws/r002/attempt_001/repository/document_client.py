import os
import boto3
from google.cloud import translate_v3 as translate
from google.cloud import aiplatform

def get_aws_textract_client():
    return boto3.client(
        'textract',
        region_name=os.environ.get('AWS_REGION', 'us-east-1'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )

def get_aws_dynamodb_client():
    return boto3.client(
        'dynamodb',
        region_name=os.environ.get('AWS_REGION', 'us-east-1'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )

def get_google_translation_client():
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or pass credentials directly
    return translate.TranslationServiceClient()

def get_google_vertex_ai_model(project_id: str, location: str, model_name: str):
    aiplatform.init(project=project_id, location=location)
    return aiplatform.GenerativeModel(model_name)

def get_google_safety_model(project_id: str, location: str, model_name: str):
    aiplatform.init(project=project_id, location=location)
    return aiplatform.GenerativeModel(model_name)
