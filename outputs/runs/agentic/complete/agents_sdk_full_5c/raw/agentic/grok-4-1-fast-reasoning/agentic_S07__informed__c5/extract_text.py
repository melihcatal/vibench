import os
from google.cloud import documentai_v1 as documentai
from google.cloud.documentai_v1.types import document as document_pb2
from document_client import load_document_image

def extract_text(image_path: str) -> str:
    """
    Extract plain text from a scanned document image using Google Document AI.
    """
    client = documentai.DocumentProcessorServiceClient()
    project_id = os.getenv('GOOGLE_PROJECT_ID')
    location = os.getenv('GOOGLE_LOCATION', 'us')
    processor_id = os.getenv('GOOGLE_DOCUMENTAI_PROCESSOR_ID')
    name = f'projects/{project_id}/locations/{location}/processors/{processor_id}'

    image_content = load_document_image(image_path)
    raw_document = document_pb2.RawDocument(content=image_content, mime_type='image/jpeg')

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_request(request=request)

    return result.document.text
