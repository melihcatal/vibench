import os
from typing import Dict
from google.cloud import documentai_v1 as documentai
from storage_client import get_b2_client, get_bucket_name


def run_ocr_on_stored_document(object_name: str, mime_type: str) -> Dict:
    b2_api = get_b2_client()
    bucket = b2_api.get_bucket_by_name(get_bucket_name())

    # Download the file from B2
    downloaded_file = bucket.download_file_by_name(object_name)
    content = downloaded_file.download()

    # Initialize Google Document AI client
    client = documentai.DocumentProcessorServiceClient()
    processor_name = os.getenv("GOOGLE_DOCUMENT_AI_PROCESSOR_NAME")
    
    # Run OCR using Google Document AI (model: "pretrained-ocr-v1.0-2020-09-23")
    raw_document = documentai.RawDocument(content=content, mime_type=mime_type)
    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)
    result = client.process_document(request=request)

    return {
        "text": result.document.text,
        "pages": [{
            "page_number": page.page_number,
            "dimensions": {
                "width": page.dimension.width,
                "height": page.dimension.height,
                "unit": page.dimension.unit
            },
            "blocks": [{
                "text": block.layout.text_anchor.content,
                "confidence": block.layout.confidence
            } for block in page.blocks]
        } for page in result.document.pages]
    }