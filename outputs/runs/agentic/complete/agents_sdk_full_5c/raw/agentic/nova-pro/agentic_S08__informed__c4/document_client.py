import os
from google.cloud import documentai

def get_document_client():
    return documentai.DocumentProcessorServiceClient()
