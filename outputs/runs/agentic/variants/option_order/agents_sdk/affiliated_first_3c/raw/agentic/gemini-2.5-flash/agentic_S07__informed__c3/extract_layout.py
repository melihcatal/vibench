from document_client import get_documentai_client, get_processor_path
from document_models import DocumentRequest, LayoutExtractionResponse
from google.cloud.documentai_v1.types import RawDocument

def extract_layout_from_document(
    document_request: DocumentRequest,
    project_id: str,
    location: str,
    processor_id: str,
) -> LayoutExtractionResponse:
    """
    Extracts layout elements (blocks, lines) from a document using Google Document AI.
    """
    client = get_documentai_client()
    processor_path = get_processor_path(project_id, location, processor_id)

    raw_document = RawDocument(content=document_request.content, mime_type=document_request.mime_type)
    
    request = {"name": processor_path, "raw_document": raw_document}
    result = client.process_document(request=request)
    
    document = result.document

    blocks = []
    lines = []
    for page in document.pages:
        for block in page.blocks:
            blocks.append(document.text[block.layout.text_anchor.text_segments[0].start_index:block.layout.text_anchor.text_segments[0].end_index])
        for line in page.lines:
            lines.append(document.text[line.layout.text_anchor.text_segments[0].start_index:line.layout.text_anchor.text_segments[0].end_index])
            
    return LayoutExtractionResponse(text_content=document.text, blocks=blocks, lines=lines)

