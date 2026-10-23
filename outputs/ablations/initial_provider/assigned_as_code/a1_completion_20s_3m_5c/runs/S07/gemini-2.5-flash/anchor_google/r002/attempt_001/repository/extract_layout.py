from typing import Dict, Any
from document_client import DocumentClient
from document_models import DocumentLayout
from google.cloud import documentai_v1 as documentai

def extract_layout(payload: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    project_id = config["project_id"]
    location = config["location"]
    processor_id = config["processor_id"]

    client = DocumentClient(project_id, location)
    processor_path = client.get_document_processor_path(processor_id)

    raw_document = documentai.RawDocument(
        content=payload["document_bytes"], mime_type=payload["mime_type"]
    )

    request = documentai.ProcessRequest(
        name=processor_path,
        raw_document=raw_document
    )

    response = client.documentai_client.process_document(request=request)
    document = response.document

    text_segments = []
    for entity in document.entities:
        if entity.text_anchor.text_segments:
            for segment in entity.text_anchor.text_segments:
                text_segments.append({
                    "start_index": segment.start_index,
                    "end_index": segment.end_index,
                    "text_content": document.text[int(segment.start_index):int(segment.end_index)]
                })

    pages = []
    for page in document.pages:
        detected_lines = []
        for paragraph in page.paragraphs:
            for line in paragraph.lines:
                line_text = documentai.get_text_anchor_text(line.text_anchor, document.text)
                detected_lines.append({
                    "text": line_text,
                    "bounding_box": [v for v in line.layout.bounding_poly.vertices]
                })
        pages.append({"lines": detected_lines})
    
    # Further processing to extract more detailed layout elements like blocks could be added here

    return {"layout": DocumentLayout(text_segments=text_segments, pages=pages)}
