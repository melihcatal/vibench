from google.cloud import documentai
from document_client import get_document_ai_client
from document_models import DocumentAIConfig, DocumentPayload

def extract_layout(payload: DocumentPayload, config: DocumentAIConfig):
    client = get_document_ai_client(config.location)
    name = client.processor_path(config.project_id, config.location, config.processor_id)
    
    raw_document = documentai.RawDocument(content=payload.document_bytes, mime_type=payload.mime_type)
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    
    response = client.process_document(request=request)
    
    # Extract layout information (pages, blocks, lines)
    document = response.document
    extracted_layout = []
    for page in document.pages:
        page_layout = {"page_number": page.page_number, "blocks": [], "lines": [], "tokens": []}
        for block in page.blocks:
            page_layout["blocks"].append(block.layout.text_anchor.text_segments[0].start_index)
        for line in page.lines:
            page_layout["lines"].append(line.layout.text_anchor.text_segments[0].start_index)
        for token in page.tokens:
            page_layout["tokens"].append(token.layout.text_anchor.text_segments[0].start_index)
        extracted_layout.append(page_layout)
            
    return {"layout": extracted_layout}
