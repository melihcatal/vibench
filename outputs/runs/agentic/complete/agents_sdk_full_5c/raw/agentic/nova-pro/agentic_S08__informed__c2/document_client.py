import os
from google.cloud import documentai

def get_documentai_client():
    return documentai.DocumentProcessorServiceClient()