import os
from document_client import (
    create_google_dai_client,
    load_image_bytes,
    get_mime_type,
    get_google_dai_processor_name,
)
from google.cloud.documentai_v1.types import ProcessRequest, RawDocument
from google.protobuf.json_format import MessageToDict


def extract_layout(image_path: str) -> list[dict]:
    client = create_google_dai_client()
    name = get_google_dai_processor_name()
    image_content = load_image_bytes(image_path)
    mime_type = get_mime_type(image_path)
    raw_document = RawDocument(content=image_content, mime_type=mime_type)
    request = ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request)
    document = result.document
    elements = []
    for page in document.pages:
        for block in page.blocks:
            bbox = [[float(v.x), float(v.y)] for v in block.bounding_poly.vertices]
            start_idx = int(block.layout.start_index)
            end_idx = int(block.layout.end_index)
            text = document.text[start_idx:end_idx].strip()
            elements.append({"type": block.type_, "text": text, "bbox": bbox})
    return elements
