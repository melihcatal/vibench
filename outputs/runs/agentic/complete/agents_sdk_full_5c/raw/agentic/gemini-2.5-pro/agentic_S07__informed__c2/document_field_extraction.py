
import os
from typing import Optional, Dict, Any
from google.api_core.client_options import ClientOptions
from google.cloud import documentai

def extract_fields_from_invoice(
    file_path: Optional[str] = None,
    file_content: Optional[bytes] = None,
    mime_type: str = "application/pdf",
) -> Dict[str, Any]:
    """
    Extracts structured fields from an invoice document using Google Document AI.
    
    Authentication is handled by GOOGLE_APPLICATION_CREDENTIALS.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = "us"  # Pre-trained models are available in specific locations
    processor_id = "pretrained-invoice-parser" # Example of a Google pre-trained model

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    name = client.processor_path(project_id, location, processor_id)

    if file_path:
        with open(file_path, "rb") as image:
            image_content = image.read()
    elif file_content:
        image_content = file_content
    else:
        raise ValueError("Either file_path or file_content must be provided.")

    raw_document = documentai.RawDocument(
        content=image_content, mime_type=mime_type
    )

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)
    
    document = result.document

    extracted_data = {"entities": []}
    for entity in document.entities:
        extracted_data["entities"].append({
            "type": entity.type_,
            "mention_text": entity.mention_text,
            "confidence": entity.confidence,
        })
    return extracted_data
