import os
from functools import lru_cache

from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from google.cloud import documentai
from openai import OpenAI
import anthropic
import cohere
import deepl
import pymongo


@lru_cache(maxsize=1)
class Settings:
    # Google Cloud Document AI
    GOOGLE_PROJECT_ID: str = os.environ.get("GOOGLE_PROJECT_ID")
    GOOGLE_LOCATION: str = os.environ.get("GOOGLE_LOCATION", "us")
    GOOGLE_PROCESSOR_ID: str = os.environ.get("GOOGLE_PROCESSOR_ID")

    # Azure Document Intelligence
    AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT: str = os.environ.get(
        "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"
    )
    AZURE_DOCUMENT_INTELLIGENCE_KEY: str = os.environ.get(
        "AZURE_DOCUMENT_INTELLIGENCE_KEY"
    )

    # OpenAI
    OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY")

    # Anthropic
    ANTHROPIC_API_KEY: str = os.environ.get("ANTHROPIC_API_KEY")
    
    # Cohere
    COHERE_API_KEY: str = os.environ.get("COHERE_API_KEY")

    # Perspective API (Google)
    PERSPECTIVE_API_KEY: str = os.environ.get("PERSPECTIVE_API_KEY")
    
    # DeepL
    DEEPL_AUTH_KEY: str = os.environ.get("DEEPL_AUTH_KEY")

    # MongoDB Atlas
    MONGO_ATLAS_URI: str = os.environ.get("MONGO_ATLAS_URI")


@lru_cache(maxsize=1)
def get_settings():
    return Settings()


def get_document_ai_client():
    opts = {"api_endpoint": f"{get_settings().GOOGLE_LOCATION}-documentai.googleapis.com"}
    return documentai.DocumentProcessorServiceClient(client_options=opts)


def get_document_intelligence_client():
    settings = get_settings()
    return DocumentAnalysisClient(
        endpoint=settings.AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT,
        credential=AzureKeyCredential(settings.AZURE_DOCUMENT_INTELLIGENCE_KEY),
    )

def get_openai_client():
    return OpenAI(api_key=get_settings().OPENAI_API_KEY)

def get_anthropic_client():
    return anthropic.Anthropic(api_key=get_settings().ANTHROPIC_API_KEY)

def get_cohere_client():
    return cohere.Client(api_key=get_settings().COHERE_API_KEY)

def get_deepl_translator():
    return deepl.Translator(auth_key=get_settings().DEEPL_AUTH_KEY)

def get_mongo_client():
    return pymongo.MongoClient(get_settings().MONGO_ATLAS_URI)

