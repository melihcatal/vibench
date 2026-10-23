import os
from google.cloud import documentai_v1 as documentai
from google.cloud import translate_v3 as translate
import boto3
import openai
import anthropic
from pymongo import MongoClient
from openai import AzureOpenAI

def get_document_ai_client():
    return documentai.DocumentProcessorServiceClient(
        client_options={"api_endpoint": os.environ.get("GOOGLE_CLOUD_DOCUMENTAI_ENDPOINT", "us-documentai.googleapis.com")}
    )

def get_textract_client():
    return boto3.client(
        "textract",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )

def get_openai_client():
    return openai.OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY")
    )

def get_anthropic_client():
    return anthropic.Anthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY")
    )

def get_azure_openai_client():
    return AzureOpenAI(
        azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
        api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-01"),
    )

def get_google_translate_client():
    return translate.TranslationServiceClient()

def get_mongodb_client():
    connection_string = os.environ.get("MONGODB_CONNECTION_STRING")
    if not connection_string:
        raise ValueError("MONGODB_CONNECTION_STRING environment variable not set")
    return MongoClient(connection_string)