import os
from openai import AzureOpenAI
from google.cloud import documentai_v1 as documentai
from google.cloud import language_v1
from google.cloud import translate_v2 as translate
from pymongo import MongoClient

def get_openai_client():
    return AzureOpenAI(
        api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
        api_version="2023-05-15",
        azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT")
    )

def get_documentai_client():
    return documentai.DocumentProcessorServiceClient()

def get_natural_language_client():
    return language_v1.LanguageServiceClient()

def get_translate_client():
    return translate.Client()

def get_mongodb_client():
    mongo_uri = os.environ.get("MONGO_DB_URI")
    return MongoClient(mongo_uri)
