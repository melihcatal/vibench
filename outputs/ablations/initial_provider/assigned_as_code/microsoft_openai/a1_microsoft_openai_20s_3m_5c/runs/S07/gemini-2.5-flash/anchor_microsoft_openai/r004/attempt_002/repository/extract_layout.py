import os
from google.cloud import documentai_v1 as documentai
from document_client import DocumentClient
from document_models import DocumentInput, ExtractedLayout

def extract_layout(document_input: DocumentInput, config: dict = None) -> ExtractedLayout:
    config = config or {}
    project_id = config.get("GOOGLE_CLOUD_PROJECT_ID") or os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = config.get("GOOGLE_CLOUD_LOCATION") or os.environ.get("GOOGLE_CLOUD_LOCATION", "us") # e.g., "us"
    processor_id = config.get("GOOGLE_CLOUD_DOCUMENT_AI_LAYOUT_PROCESSOR_ID")

    if not all([project_id, location, processor_id]):
        raise ValueError("Google Cloud project ID, location, or layout processor ID not provided.")

    document_client_helper = DocumentClient(config)
    client = document_client_helper.get_google_document_ai_client()

    name = client.processor_path(project_id, location, processor_id)

    # Convert bytes to a documentai.RawDocument
    raw_document = documentai.RawDocument(
        content=document_input.document_bytes,
        mime_type=document_input.mime_type,
    )

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)
    document = result.document

    pages_data = []
    for page in document.pages:
        page_layout = {
            "page_number": page.page_number,
            "dimension": {"width": page.dimension.width, "height": page.dimension.height, "unit": page.dimension.unit},
            "lines": [],
            "paragraphs": [],
            "blocks": []
        }

        for paragraph in page.paragraphs:
            page_layout["paragraphs"].append({"text": documentai.get_text_anchor_text(paragraph.layout.text_anchor, document.text)})

        for block in page.blocks:
            page_layout["blocks"].append({"text": documentai.get_text_anchor_text(block.layout.text_anchor, document.text)})
            
        for line in page.lines:
            page_layout["lines"].append({"text": documentai.get_text_anchor_text(line.layout.text_anchor, document.text)})

        pages_data.append(page_layout)

    return ExtractedLayout(pages=pages_data)
