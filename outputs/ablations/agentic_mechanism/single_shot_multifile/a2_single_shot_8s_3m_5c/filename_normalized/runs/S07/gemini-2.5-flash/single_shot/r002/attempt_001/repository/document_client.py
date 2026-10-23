import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import google.cloud.translate_v3 as translate
import openai
import cohere

def get_azure_document_intelligence_client() -> DocumentAnalysisClient:
    endpoint = os.environ.get("AZURE_DI_ENDPOINT")
    key = os.environ.get("AZURE_DI_KEY")
    if not endpoint or not key:
        raise ValueError("AZURE_DI_ENDPOINT and AZURE_DI_KEY must be set in environment variables.")
    return DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def get_google_translate_client() -> translate.TranslationServiceClient:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ.get("GOOGLE_TRANSLATE_CREDENTIALS_PATH")
    if not os.environ.get("GOOGLE_TRANSLATE_PROJECT_ID"):
        raise ValueError("GOOGLE_TRANSLATE_PROJECT_ID must be set in environment variables.")
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        raise ValueError("GOOGLE_TRANSLATE_CREDENTIALS_PATH must be set in environment variables.")
    return translate.TranslationServiceClient()

def set_openai_api_key():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY must be set in environment variables.")
    openai.api_key = api_key

def get_cohere_client() -> cohere.Client:
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY must be set in environment variables.")
    return cohere.Client(api_key)
