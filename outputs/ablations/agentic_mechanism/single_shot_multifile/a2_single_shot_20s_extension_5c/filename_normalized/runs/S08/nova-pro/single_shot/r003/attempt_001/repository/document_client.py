import os
from google.cloud import documentai

def get_documentai_client():
    return documentai.DocumentProcessorServiceClient()

def get_processor_id():
    return os.getenv('DOCUMENTAI_PROCESSOR_ID', 'b1a8221621204655')

def get_project_id():
    return os.getenv('GOOGLE_CLOUD_PROJECT')