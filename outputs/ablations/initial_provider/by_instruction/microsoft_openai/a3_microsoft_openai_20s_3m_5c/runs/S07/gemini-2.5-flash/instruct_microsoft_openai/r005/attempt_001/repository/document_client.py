
import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from openai import AzureOpenAI

def get_azure_vision_client():
    endpoint = os.environ.get("AZURE_AI_VISION_ENDPOINT")
    key = os.environ.get("AZURE_AI_VISION_KEY")
    if not endpoint or not key:
        raise ValueError("AZURE_AI_VISION_ENDPOINT and AZURE_AI_VISION_KEY environment variables must be set.")
    return ImageAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def get_document_intelligence_client():
    endpoint = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY")
    if not endpoint or not key:
        raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY environment variables must be set.")
    return DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def get_azure_translator_client():
    endpoint = os.environ.get("AZURE_TRANSLATOR_ENDPOINT")
    key = os.environ.get("AZURE_TRANSLATOR_KEY")
    region = os.environ.get("AZURE_TRANSLATOR_REGION")
    if not endpoint or not key or not region:
        raise ValueError("AZURE_TRANSLATOR_ENDPOINT, AZURE_TRANSLATOR_KEY, and AZURE_TRANSLATOR_REGION environment variables must be set.")
    return TextTranslationClient(endpoint=endpoint, credential=TranslatorCredential(key, region))

def get_azure_content_safety_client():
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")
    return ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def get_azure_openai_client():
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    key = os.environ.get("AZURE_OPENAI_KEY")
    if not endpoint or not key:
        raise ValueError("AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_KEY environment variables must be set.")
    return AzureOpenAI(
        api_key=key,
        api_version="2024-02-01",
        azure_endpoint=endpoint
    )
