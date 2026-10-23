"""
document_client.py

Provide local configuration and client helper utilities for Structured Document Extraction
using Google Document AI.
"""

import os
from google.cloud import documentai_v1 as documentai

def get_documentai_client():
    """
    Initializes and returns a Google Document AI client.
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable to be set.
    """
    client_options = {"api_endpoint": "us-documentai.googleapis.com"}
    return documentai.DocumentProcessorServiceClient(client_options=client_options)

def process_document(client, project_id: str, location: str, processor_id: str, file_content: bytes, mime_type: str):
    """
    Sends a document to a specified Document AI processor for processing.
    """
    name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    raw_document = documentai.RawDocument(
        content=file_content,
        mime_type=mime_type,
    )

    # Configure the process request
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)
    return result.document
