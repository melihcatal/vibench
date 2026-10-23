from google.cloud import documentai_v1 as documentai
import os
from document_client import load_image_bytes
from document_models import LayoutResult


def extract_layout(image_path: str) -> LayoutResult:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = "us"
    processor_id = os.getenv("DOCUMENTAI_PROCESSOR_ID")
    client = documentai.DocumentProcessorServiceClient()
    name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"
    content = load_image_bytes(image_path)
    raw_document = documentai.RawDocument(content=content, mime_type="image/jpeg")
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    result = client.process_document(request=request)
    document = result.document
    blocks = []
    for page in document.pages:
        for block in page.blocks or []:
            blocks.append(
                {
                    "type": block.type_,
                    "text": block.text_anchor.content if block.text_anchor else "",
                    "confidence": block.confidence,
                    "bounding_box": [
                        {"x": vertex.x, "y": vertex.y}
                        for vertex in block.layout.vertices
                    ],
                }
            )
    return {"blocks": blocks}
