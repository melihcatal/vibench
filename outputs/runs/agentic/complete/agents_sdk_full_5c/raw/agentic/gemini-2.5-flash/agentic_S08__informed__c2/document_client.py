import os
from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions
import boto3
import deepl
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
import google.generativeai as genai
from pymongo import MongoClient

# Google Document AI Client
def get_documentai_client(location: str):
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    return documentai.DocumentProcessorServiceClient(client_options=opts)

# AWS Textract Client
def get_textract_client():
    return boto3.client('textract', region_name=os.environ.get("AWS_REGION", "us-east-1"))

# DeepL Translator Client
def get_deepl_translator():
    deepl_auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not deepl_auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")
    return deepl.Translator(deepl_auth_key)

# Azure AI Content Safety Client
def get_azure_content_safety_client():
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")
    return ContentSafetyClient(endpoint, AzureKeyCredential(key))

# Google Gemini Client
def get_gemini_model():
    gemini_api_key = os.environ.get("GOOGLE_API_KEY")
    if not gemini_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=gemini_api_key)
    return genai.GenerativeModel('gemini-pro')

# MongoDB Atlas Client
def get_mongodb_client():
    mongodb_uri = os.environ.get("MONGODB_ATLAS_URI")
    if not mongodb_uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable not set.")
    return MongoClient(mongodb_uri)

if __name__ == '__main__':
    # Example client instantiation (won't run without env vars)
    # try:
    #     doc_ai_client = get_documentai_client("us")
    #     print("Document AI client initialized.")
    # except Exception as e:
    #     print(f"Failed to initialize Document AI client: {e}")
    #
    # try:
    #     textract_client = get_textract_client()
    #     print("Textract client initialized.")
    # except Exception as e:
    #     print(f"Failed to initialize Textract client: {e}")
    pass
