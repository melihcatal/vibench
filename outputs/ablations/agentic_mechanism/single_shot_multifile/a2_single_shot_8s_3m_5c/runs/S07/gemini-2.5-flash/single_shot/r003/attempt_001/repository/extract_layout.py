import os
from typing import List, Optional

from google.cloud import documentai_v1 as documentai

from document_client import get_gcp_documentai_processor_path
from document_models import DocumentInput, LayoutExtractionOutput, LayoutElement

def extract_document_layout(
    document_input: DocumentInput,
    processor_id: Optional[str] = None,
) -> LayoutExtractionOutput:
    """Extracts layout elements (blocks, lines, paragraphs) using Google Cloud Document AI."""
    project_id = os.environ.get("GCP_PROJECT_ID")
    location = os.environ.get("GCP_LOCATION", "us") # Or other relevant location
    default_processor_id = os.environ.get("GCP_DOCUMENTAI_OCR_PROCESSOR_ID", "OCR_PROCESSOR_ID_HERE")

    processor_name = get_gcp_documentai_processor_path(
        project_id, location, processor_id or default_processor_id
    )

    client = documentai.DocumentProcessorServiceClient()

    raw_document = documentai.RawDocument(
        content=document_input.image_bytes,
        mime_type=document_input.mime_type,
    )
    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)

    response = client.process_document(request=request)
    document = response.document

    extracted_elements: List[LayoutElement] = []

    for page in document.pages:
        # Extract paragraphs
        for paragraph in page.paragraphs:
            text = documentai.get_text_anchor_text(paragraph.layout.text_anchor, document.text)
            bounding_box = [vertex.x, vertex.y for vertex in paragraph.layout.bounding_poly.vertices]
            extracted_elements.append(LayoutElement(type="paragraph", text=text, bounding_box=bounding_box))

        # Extract lines
        for line in page.lines:
            text = documentai.get_text_anchor_text(line.layout.text_anchor, document.text)
            bounding_box = [vertex.x, vertex.y for vertex in line.layout.bounding_poly.vertices]
            extracted_elements.append(LayoutElement(type="line", text=text, bounding_box=bounding_box))

        # Extract tokens (words)
        for token in page.tokens:
            text = documentai.get_text_anchor_text(token.layout.text_anchor, document.text)
            bounding_box = [vertex.x, vertex.y for vertex in token.layout.bounding_poly.vertices]
            extracted_elements.append(LayoutElement(type="token", text=text, bounding_box=bounding_box))

    return LayoutExtractionOutput(elements=extracted_elements)
