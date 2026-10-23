import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.documentintelligence import DocumentAnalysisClient
from azure.ai.documentintelligence.models import AnalyzeResult
from azure.core.credentials import AzureKeyCredential

def get_document_analysis_client():
    endpoint = os.environ.get("AZURE_VISION_ENDPOINT")
    key = os.environ.get("AZURE_VISION_KEY")
    if not endpoint or not key:
        raise ValueError("AZURE_VISION_ENDPOINT and AZURE_VISION_KEY environment variables must be set.")
    return ImageAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def get_document_intelligence_client():
    endpoint = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY")
    if not endpoint or not key:
        raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY environment variables must be set.")
    return DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def get_translator_client():
    from azure.ai.translation.text import TextTranslationClient, TextTranslationApiVersion
    from azure.core.credentials import AzureKeyCredential

    endpoint = os.environ.get("AZURE_TRANSLATOR_ENDPOINT")
    key = os.environ.get("AZURE_TRANSLATOR_KEY")
    region = os.environ.get("AZURE_TRANSLATOR_REGION")
    if not endpoint or not key or not region:
        raise ValueError("AZURE_TRANSLATOR_ENDPOINT, AZURE_TRANSLATOR_KEY, and AZURE_TRANSLATOR_REGION environment variables must be set.")
    return TextTranslationClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
        region=region,
        api_version=TextTranslationApiVersion.V3_0
    )

def get_content_safety_client():
    from azure.ai.contentsafety import ContentSafetyClient
    from azure.core.credentials import AzureKeyCredential

    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set.")
    return ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def get_openai_client():
    from openai import AzureOpenAI

    azure_openai_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    azure_openai_key = os.environ.get("AZURE_OPENAI_KEY")
    azure_openai_api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-01")

    if not azure_openai_endpoint or not azure_openai_key:
        raise ValueError("AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_KEY environment variables must be set.")

    return AzureOpenAI(
        azure_endpoint=azure_openai_endpoint,
        api_key=azure_openai_key,
        api_version=azure_openai_api_version
    )
