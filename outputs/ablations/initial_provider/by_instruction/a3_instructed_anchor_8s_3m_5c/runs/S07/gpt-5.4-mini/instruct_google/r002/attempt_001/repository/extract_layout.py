from google.cloud import documentai_v1 as documentai

from document_client import build_documentai_name, load_config
from document_models import DocumentInput, LayoutElement, serialize_layout


def extract_layout(document: DocumentInput):
    config = load_config()
    client = documentai.DocumentProcessorServiceClient()
    name = build_documentai_name(config.gcp_project_id, config.gcp_location, config.gcp_layout_processor_id or config.gcp_processor_id)
    request = documentai.ProcessRequest(name=name, raw_document=documentai.RawDocument(content=document.content, mime_type=document.mime_type))
    response = client.process_document(request=request)
    elements = []
    for page in getattr(response.document, "pages", []):
        for block in getattr(page, "blocks", []):
            elements.append(LayoutElement(type="block", text=getattr(block.layout, "text_anchor", None) and str(block.layout.text_anchor), confidence=getattr(block.layout, "confidence", None)))
        for line in getattr(page, "lines", []):
            elements.append(LayoutElement(type="line", text=getattr(line.layout, "text_anchor", None) and str(line.layout.text_anchor), confidence=getattr(line.layout, "confidence", None)))
    return serialize_layout(elements)
