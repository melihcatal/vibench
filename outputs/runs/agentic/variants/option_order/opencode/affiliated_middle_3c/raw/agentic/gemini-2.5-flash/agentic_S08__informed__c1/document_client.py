import os
import boto3
from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions
import google.generativeai as genai
from mistralai.client import MistralClient
from anthropic import Anthropic
import deepl
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from pymongo import MongoClient


def get_google_documentai_client(location: str):
    """Provides a configured Google Document AI client."""
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    return documentai.DocumentProcessorServiceClient(client_options=opts)


def get_aws_textract_client(region_name: str = "us-east-1"):
    """Provides a configured AWS Textract client."""
    return boto3.client("textract", region_name=region_name)


def configure_gemini_api():
    """Configures Google Gemini API."""
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))


def get_mistral_client():
    """Provides a configured Mistral AI client."""
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY environment variable not set.")
    return MistralClient(api_key=api_key)


def get_anthropic_client():
    """Provides a configured Anthropic client."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set.")
    return Anthropic(api_key=api_key)


def get_azure_content_safety_client():
    """Provides a configured Azure AI Content Safety client."""
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables not set."
        )
    return ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))


def get_deepl_translator():
    """Provides a configured DeepL Translator client."""
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")
    return deepl.Translator(auth_key)


def get_mongodb_client():
    """Provides a configured MongoDB Atlas client."""
    mongo_uri = os.environ.get("MONGODB_ATLAS_URI")
    if not mongo_uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable not set.")
    return MongoClient(mongo_uri)


if __name__ == "__main__":
    print("Client helper utilities for Structured Document Extraction are available.")
