import os
from google.cloud import documentai

def get_client():
    return documentai.DocumentProcessorServiceClient()

def get_project_id():
    return os.getenv('GOOGLE_CLOUD_PROJECT')

def get_location():
    return 'us'

def get_processor_id():
    return os.getenv('DOCUMENTAI_PROCESSOR_ID')