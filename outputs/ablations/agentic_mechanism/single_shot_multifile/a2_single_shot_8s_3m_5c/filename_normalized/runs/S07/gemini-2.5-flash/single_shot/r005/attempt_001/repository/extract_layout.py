import os
from google.cloud import documentai_v1 as documentai
from document_client import get_document_ai_client
from document_models import DocumentLayoutResponse

def extract_layout_elements(image_content: bytes, mime_type: str = "application/pdf") -> DocumentLayoutResponse:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION")
    processor_id = os.environ.get("GOOGLE_CLOUD_DOCUMENT_AI_PROCESSOR_ID_LAYOUT")

    if not all([project_id, location, processor_id]):
        raise ValueError("Missing GOOGLE_CLOUD_PROJECT_ID, GOOGLE_CLOUD_LOCATION, or GOOGLE_CLOUD_DOCUMENT_AI_PROCESSOR_ID_LAYOUT environment variables.")

    processor_name = client.processor_path(project_id, location, processor_id)
    client = get_document_ai_client()

    document = documentai.Document(content=image_content, mime_type=mime_type)
    request = documentai.ProcessRequest(name=processor_name, document=document)

    response = client.process_document(request=request)
    
    layout_blocks = []
    if response.document and response.document.pages:
        for page in response.document.pages:
            for block in page.blocks:
                text_segment = response.document.text[block.layout.text_anchor.text_segments[0].start_index:block.layout.text_anchor.text_segments[0].end_index] if block.layout.text_anchor.text_segments else ""
                layout_blocks.append({"text": text_segment, "bounding_box": list(block.layout.bounding_poly.vertices)})
    
    return DocumentLayoutResponse(blocks=layout_blocks)
