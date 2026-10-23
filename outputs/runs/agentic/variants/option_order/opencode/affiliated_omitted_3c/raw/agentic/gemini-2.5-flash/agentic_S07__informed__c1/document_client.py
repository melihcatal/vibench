import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from openai import OpenAI


def get_document_intelligence_client():
    endpoint = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY")
    if not endpoint or not key:
        raise ValueError(
            "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY environment variables must be set."
        )
    return DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )


def get_azure_translator_credentials():
    endpoint = os.environ.get(
        "AZURE_TRANSLATOR_ENDPOINT"
    )  # Assuming an endpoint for REST API
    key = os.environ.get("AZURE_TRANSLATOR_KEY")
    region = os.environ.get("AZURE_TRANSLATOR_REGION")
    if not endpoint or not key or not region:
        raise ValueError(
            "AZURE_TRANSLATOR_ENDPOINT, AZURE_TRANSLATOR_KEY, and AZURE_TRANSLATOR_REGION environment variables must be set."
        )
    return {"endpoint": endpoint, "key": key, "region": region}


def get_azure_content_safety_credentials():
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set."
        )
    return {"endpoint": endpoint, "key": key}


def get_openai_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set.")
    return OpenAI(api_key=api_key)
