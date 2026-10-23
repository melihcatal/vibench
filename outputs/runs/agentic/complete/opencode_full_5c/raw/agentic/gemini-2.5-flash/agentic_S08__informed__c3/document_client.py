import os
from google.cloud import documentai_v1 as documentai
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
import google.generativeai as genai
import anthropic
from mistralai.client import MistralClient
import requests
import deepl
from google.cloud import firestore


def get_gcp_project_id() -> str:
    return os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")


def get_documentai_processor_id() -> str:
    return os.environ.get(
        "DOCUMENTAI_INVOICE_PROCESSOR_ID", "your-documentai-invoice-processor-id"
    )


def get_azure_document_intelligence_endpoint() -> str:
    return os.environ.get(
        "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT",
        "https://your-endpoint.cognitiveservices.azure.com/",
    )


def get_azure_document_intelligence_key() -> str:
    return os.environ.get(
        "AZURE_DOCUMENT_INTELLIGENCE_KEY", "your-azure-document-intelligence-key"
    )


def get_google_api_key() -> str:
    return os.environ.get("GOOGLE_API_KEY", "your-google-api-key")


def get_anthropic_api_key() -> str:
    return os.environ.get("ANTHROPIC_API_KEY", "your-anthropic-api-key")


def get_mistral_api_key() -> str:
    return os.environ.get("MISTRAL_API_KEY", "your-mistral-api-key")


def get_azure_content_safety_endpoint() -> str:
    return os.environ.get(
        "AZURE_CONTENT_SAFETY_ENDPOINT",
        "https://your-content-safety-endpoint.cognitiveservices.azure.com/",
    )


def get_azure_content_safety_key() -> str:
    return os.environ.get("AZURE_CONTENT_SAFETY_KEY", "your-azure-content-safety-key")


def get_deepl_auth_key() -> str:
    return os.environ.get("DEEPL_AUTH_KEY", "your-deepl-auth-key")


def get_documentai_client():
    return documentai.DocumentProcessorServiceClient()


def get_azure_document_intelligence_client():
    endpoint = get_azure_document_intelligence_endpoint()
    key = get_azure_document_intelligence_key()
    return DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )


def get_gemini_model(model_name: str = "gemini-pro"):
    genai.configure(api_key=get_google_api_key())
    return genai.GenerativeModel(model_name)


def get_anthropic_client():
    return anthropic.Anthropic(api_key=get_anthropic_api_key())


def get_mistral_client():
    return MistralClient(api_key=get_mistral_api_key())


def get_deepl_translator():
    return deepl.Translator(get_deepl_auth_key())


def get_firestore_client():
    return firestore.Client()
