import os
from google.cloud import documentai_v1 as documentai

def get_document_ai_client():
    return documentai.DocumentProcessorServiceClient()

def get_document_ai_processor_path(project_id, location, processor_id):
    return documentai.DocumentProcessorServiceClient.processor_path(
        project_id, location, processor_id
    )
