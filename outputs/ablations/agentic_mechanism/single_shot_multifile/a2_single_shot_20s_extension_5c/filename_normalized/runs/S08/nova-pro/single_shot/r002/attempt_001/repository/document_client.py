import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

def get_document_client():
    endpoint = os.getenv('FORM_RECOGNIZER_ENDPOINT')
    key = os.getenv('FORM_RECOGNIZER_KEY')
    return DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))