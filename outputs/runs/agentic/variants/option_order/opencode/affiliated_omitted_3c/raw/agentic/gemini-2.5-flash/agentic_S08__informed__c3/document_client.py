import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from openai import OpenAI
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from azure.core.credentials import AzureKeyCredential as AzureContentSafetyKeyCredential
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.cosmos import CosmosClient


def get_document_intelligence_client():
    endpoint = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY")
    if not endpoint or not key:
        raise ValueError(
            "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY must be set"
        )
    return DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))


def get_openai_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY must be set")
    return OpenAI(api_key=api_key)


def get_azure_content_safety_client():
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set"
        )
    return ContentSafetyClient(
        endpoint=endpoint, credential=AzureContentSafetyKeyCredential(key)
    )


def get_azure_translator_client():
    endpoint = os.environ.get(
        "AZURE_TRANSLATOR_ENDPOINT"
    )  # Note: Azure AI Translator uses a region, not a full endpoint in some SDKs, but a full endpoint if using a custom subdomain.
    key = os.environ.get("AZURE_TRANSLATOR_KEY")
    region = os.environ.get("AZURE_TRANSLATOR_REGION")
    if not endpoint or not key or not region:
        raise ValueError(
            "AZURE_TRANSLATOR_ENDPOINT, AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_REGION must be set"
        )
    return TextTranslationClient(
        endpoint=endpoint, credential=TranslatorCredential(key, region)
    )


def get_cosmos_client():
    endpoint = os.environ.get("AZURE_COSMOS_ENDPOINT")
    key = os.environ.get("AZURE_COSMOS_KEY")
    if not endpoint or not key:
        raise ValueError("AZURE_COSMOS_ENDPOINT and AZURE_COSMOS_KEY must be set")
    return CosmosClient(url=endpoint, credential=key)
