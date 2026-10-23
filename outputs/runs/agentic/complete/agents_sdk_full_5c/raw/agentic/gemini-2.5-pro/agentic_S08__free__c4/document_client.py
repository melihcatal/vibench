# document_client.py
import os
from functools import lru_cache

# Dummy configuration loader
def get_config():
    return {
        "azure_document_intelligence_endpoint": os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"),
        "azure_document_intelligence_key": os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY"),
        "google_application_credentials": os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"),
        "gcp_project_id": os.environ.get("GCP_PROJECT_ID"),
        "gcp_location": os.environ.get("GCP_LOCATION"),
        "gcp_processor_id": os.environ.get("GCP_PROCESSOR_ID"),
        "openai_api_key": os.environ.get("OPENAI_API_KEY"),
        "anthropic_api_key": os.environ.get("ANTHROPIC_API_KEY"),
        "cohere_api_key": os.environ.get("COHERE_API_KEY"),
        "azure_content_safety_endpoint": os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT"),
        "azure_content_safety_key": os.environ.get("AZURE_CONTENT_SAFETY_KEY"),
        "mongo_atlas_uri": os.environ.get("MONGO_ATLAS_URI"),
    }

@lru_cache(maxsize=1)
def get_azure_document_intelligence_client():
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.formrecognizer import DocumentAnalysisClient

    config = get_config()
    endpoint = config["azure_document_intelligence_endpoint"]
    key = config["azure_document_intelligence_key"]
    if not endpoint or not key:
        raise ValueError("Azure Document Intelligence credentials not configured.")
    return DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

@lru_cache(maxsize=1)
def get_google_document_ai_client():
    from google.cloud import documentai

    config = get_config()
    if not config.get("google_application_credentials"):
        raise ValueError("Google Application Credentials not configured.")
    
    opts = {"api_endpoint": f"{config['gcp_location']}-documentai.googleapis.com"}
    return documentai.DocumentProcessorServiceClient(client_options=opts)

@lru_cache(maxsize=1)
def get_openai_client():
    from openai import OpenAI
    config = get_config()
    if not config.get("openai_api_key"):
        raise ValueError("OpenAI API key not configured.")
    return OpenAI(api_key=config["openai_api_key"])

@lru_cache(maxsize=1)
def get_anthropic_client():
    from anthropic import Anthropic
    config = get_config()
    if not config.get("anthropic_api_key"):
        raise ValueError("Anthropic API key not configured.")
    return Anthropic(api_key=config["anthropic_api_key"])

@lru_cache(maxsize=1)
def get_cohere_client():
    import cohere
    config = get_config()
    if not config.get("cohere_api_key"):
        raise ValueError("Cohere API key not configured.")
    return cohere.Client(config["cohere_api_key"])

@lru_cache(maxsize=1)
def get_azure_content_safety_client():
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.contentsafety import ContentSafetyClient
    config = get_config()
    endpoint = config.get("azure_content_safety_endpoint")
    key = config.get("azure_content_safety_key")
    if not endpoint or not key:
        raise ValueError("Azure Content Safety credentials not configured.")
    return ContentSafetyClient(endpoint, AzureKeyCredential(key))

@lru_cache(maxsize=1)
def get_google_translate_client():
    from google.cloud import translate_v2 as translate
    config = get_config()
    if not config.get("google_application_credentials"):
        raise ValueError("Google Application Credentials not configured.")
    return translate.Client()

@lru_cache(maxsize=1)
def get_mongo_atlas_client():
    from pymongo import MongoClient
    config = get_config()
    uri = config.get("mongo_atlas_uri")
    if not uri:
        raise ValueError("MongoDB Atlas URI not configured.")
    # Example URI: mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/
    return MongoClient(uri)
