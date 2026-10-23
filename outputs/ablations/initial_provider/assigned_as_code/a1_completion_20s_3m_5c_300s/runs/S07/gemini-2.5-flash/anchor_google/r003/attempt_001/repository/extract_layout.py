from google.cloud import documentai_v1 as documentai
from document_client import get_documentai_client
from document_models import DocumentPayload, DocumentConfig, LayoutExtractionResult


def extract_layout(payload: DocumentPayload, config: DocumentConfig) -> LayoutExtractionResult:
    client = get_documentai_client(config.location)
    name = client.processor_path(config.project_id, config.location, config.processor_id)
    
    raw_document = documentai.RawDocument(
        content=payload.document_bytes, mime_type=payload.mime_type
    )
    
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    response = client.process_document(request=request)
    
    document = response.document
    
    pages_data = []
    for page in document.pages:
        page_text = "".join([text_element.text_segment.text for text_element in page.tokens])
        pages_data.append({
            "page_number": page.page_number,
            "dimension": {"width": page.dimension.width, "height": page.dimension.height},
            "text": page_text,
            "blocks": [{
                "bbox": [v.x, v.y for v in block.layout.bounding_poly.vertices],
                "text_segments": [{
                    "start_index": ts.start_index, "end_index": ts.end_index
                } for ts in block.layout.text_anchor.text_segments]
            } for block in page.blocks],
            "lines": [{
                "bbox": [v.x, v.y for v in line.layout.bounding_poly.vertices],
                "text_segments": [{
                    "start_index": ts.start_index, "end_index": ts.end_index
                } for ts in line.layout.text_anchor.text_segments]
            } for line in page.lines],
        })

    entities_data = []
    for entity in document.entities:
        entities_data.append({
            "type": entity.type,
            "mention_text": entity.mention_text,
            "confidence": entity.confidence,
            "bounding_poly": [v.x, v.y for v in entity.bounding_poly.vertices] if entity.bounding_poly else []
        })

    return LayoutExtractionResult(
        text=document.text,
        pages=pages_data,
        entities=entities_data
    )
