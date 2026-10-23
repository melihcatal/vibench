import os
import boto3 # AWS SDK import
from openai import OpenAI
from google.cloud import documentai_v1beta3 as documentai # Google Cloud Document AI SDK
from google.api_core.client_options import ClientOptions
from google.cloud import language_v1 # Google Cloud Natural Language SDK
from google.cloud import translate_v2 as translate # Google Cloud Translate SDK
from google.cloud import firestore # Google Cloud Firestore SDK
import requests # For Perspective API

def get_openai_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    return OpenAI(api_key=api_key)

def get_aws_textract_client():
    # AWS Textract client
    # AWS Region and credentials can be configured via environment variables or AWS CLI
    return boto3.client('textract', region_name=os.environ.get("AWS_REGION", "us-east-1"))

def get_google_documentai_client():
    # Google Cloud Document AI client
    # Project ID and Location can be configured via environment variables
    # Or ensure GOOGLE_APPLICATION_CREDENTIALS points to a valid service account key file
    return documentai.DocumentProcessorServiceClient(
        client_options=ClientOptions(api_endpoint=f"{os.environ.get("GCP_REGION", "us")}-documentai.googleapis.com")
    )

def get_google_nl_client():
    # Google Cloud Natural Language client
    return language_v1.LanguageServiceClient()

def get_perspective_api_client():
    # Perspective API is a REST API. We'll use requests to interact with it.
    # API hostname: commentanalyzer.googleapis.com
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")
    return {"api_key": api_key, "api_endpoint": "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"}

def get_google_translate_client():
    # Google Cloud Translation client (v2)
    return translate.Client()

def get_google_firestore_client():
    # Google Cloud Firestore client
    # Project ID can be configured via environment variable GOOGLE_CLOUD_PROJECT or GOOGLE_APPLICATION_CREDENTIALS
    return firestore.Client()


