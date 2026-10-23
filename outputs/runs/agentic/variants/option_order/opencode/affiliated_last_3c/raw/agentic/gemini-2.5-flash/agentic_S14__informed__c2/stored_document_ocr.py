import os
from typing import List, Dict
from google.cloud import documentai_v1beta3 as documentai
from storage_client import StorageClient


def run_ocr_on_stored_document(
    project_id: str, location: str, processor_id: str, gcs_input_uri: str
) -> Dict:
    """Runs OCR on a document stored in Google Cloud Storage using Google Document AI.

    Args:
        project_id (str): Your Google Cloud project ID.
        location (str): The location of the processor (e.g., "us").
        processor_id (str): The ID of the Document AI processor to use.
        gcs_input_uri (str): The Google Cloud Storage URI of the input document
                               (e.g., "gs://your-bucket/your-document.pdf").

    Returns:
        Dict: A dictionary containing the extracted text and other information.
    """
    documentai_client = StorageClient.get_documentai_client()

    # The full resource name of the processor
    # e.g.: projects/project_id/locations/location/processors/processor_id
    name = documentai_client.processor_path(project_id, location, processor_id)

    # Configure the input document
    gcs_document = documentai.GcsDocument(gcs_uri=gcs_input_uri)
    input_config = documentai.DocumentInputConfig(gcs_document=gcs_document)

    # Configure the process request
    request = documentai.ProcessRequest(name=name, input_document=input_config)

    print(f"Sending OCR request for {gcs_input_uri} using processor {name}...")
    result = documentai_client.process_document(request=request)

    document = result.document
    text = document.text

    pages_data = []
    for page in document.pages:
        page_text = (
            page.layout.text_anchor.text_segments[0].end_index
            if page.layout
            and page.layout.text_anchor
            and page.layout.text_anchor.text_segments
            else None
        )
        pages_data.append({"page_number": page.page_number, "text": page_text})

    print(f"OCR completed. Extracted {len(text)} characters.")

    return {
        "full_text": text,
        "pages": pages_data,
        "document_entities": [],
    }  # Simplified return, Document AI has more entities
