
import os
from google.cloud import documentai_v1 as documentai
from google.cloud import translate_v3 as translate
from google.cloud import language_v1 as language
import boto3
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import openai
import cohere

def get_documentai_client():
    return documentai.DocumentProcessorServiceClient()

def get_textract_client():
    return boto3.client('textract', region_name=os.environ.get("AWS_REGION"))

def get_azure_document_intelligence_client(endpoint, api_key):
    return DocumentAnalysisClient(endpoint, AzureKeyCredential(api_key))

def get_translation_client():
    return translate.TranslationServiceClient()

def get_language_client():
    return language.LanguageServiceClient()

def get_openai_client(api_key):
    return openai.OpenAI(api_key=api_key)

def get_cohere_client(api_key):
    return cohere.Client(api_key=api_key)
