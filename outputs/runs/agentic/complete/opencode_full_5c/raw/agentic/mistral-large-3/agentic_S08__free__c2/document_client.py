from typing import Dict, Any, List, Optional
import os
from google.cloud import documentai_v1 as documentai
from google.api_core.client_options import ClientOptions


def get_document_client() -> documentai.DocumentProcessorServiceClient:
    """Initialize and return a Google Cloud Document AI client."""
    processor_id = os.getenv("GOOGLE_DOCUMENT_AI_PROCESSOR_ID", "your-processor-id")
    location = os.getenv("GOOGLE_DOCUMENT_AI_LOCATION", "us")
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "your-project-id")

    client_options = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=client_options)

    return client, processor_id, location, project_id


def process_document(
    file_path: str, mime_type: str = "application/pdf"
) -> documentai.Document:
    """Process a document using Google Cloud Document AI and return the parsed document."""
    client, processor_id, location, project_id = get_document_client()

    with open(file_path, "rb") as file:
        document_content = file.read()

    resource_name = client.processor_path(project_id, location, processor_id)
    request = documentai.ProcessRequest(
        name=resource_name,
        raw_document=documentai.RawDocument(
            content=document_content, mime_type=mime_type
        ),
    )

    result = client.process_document(request=request)
    return result.document
