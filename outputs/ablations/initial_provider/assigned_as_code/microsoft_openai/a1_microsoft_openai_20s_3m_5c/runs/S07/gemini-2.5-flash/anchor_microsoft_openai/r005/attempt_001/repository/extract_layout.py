
import os
from google.cloud import documentai_v1 as documentai
from document_client import get_documentai_client
from document_models import DocumentLayoutBlock, DocumentExtractionResult

def extract_layout(payload, config=None):
    config = config or {}
    client = get_documentai_client()
    
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us") # e.g., "us"
    processor_id = config.get("DOCUMENTAI_LAYOUT_PROCESSOR_ID")
    
    if not all([project_id, location, processor_id]):
        raise ValueError("Missing GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION, or DOCUMENTAI_LAYOUT_PROCESSOR_ID environment variables/config.")

    name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    document = documentai.RawDocument(content=payload['document_bytes'], mime_type=payload['mime_type'])

    # Configure the process request
    request = documentai.ProcessRequest(
        name=name,
        raw_document=document,
        # Optional: Additional fields for OcrConfig, etc.
    )

    result = client.process_document(request=request).document

    layout_blocks = []
    for page in result.pages:
        for paragraph in page.paragraphs:
            layout_blocks.append(DocumentLayoutBlock(
                text=paragraph.layout.text_anchor.content,
                bounding_boxes=[
                    paragraph.layout.bounding_poly.vertices[0].x,
                    paragraph.layout.bounding_poly.vertices[0].y,
                    paragraph.layout.bounding_poly.vertices[1].x,
                    paragraph.layout.bounding_poly.vertices[1].y,
                    paragraph.layout.bounding_poly.vertices[2].x,
                    paragraph.layout.bounding_poly.vertices[2].y,
                    paragraph.layout.bounding_poly.vertices[3].x,
                    paragraph.layout.bounding_poly.vertices[3].y,
                ]
            ))
        # Add more layout elements like lines, form_fields, etc. as needed

    return DocumentExtractionResult(
        text_content=result.text,
        layout_blocks=layout_blocks
    )
