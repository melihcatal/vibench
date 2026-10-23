from google.cloud import documentai_v1 as documentai
from document_client import DOCAI_PROJECT_ID, DOCAI_LOCATION, DOCAI_PROCESSOR_ID
from document_models import LayoutElement, BoundingBox
from typing import List

def extract_layout(image_path: str) -> List[LayoutElement]:
    """Extracts blocks, lines, tables, or layout elements from a document."""
    client = documentai.DocumentProcessorServiceClient()
    name = f"projects/{DOCAI_PROJECT_ID}/locations/{DOCAI_LOCATION}/processors/{DOCAI_PROCESSOR_ID}"
    
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    
    raw_document = documentai.RawDocument(
        content=content, 
        mime_type='image/jpeg'
    )
    request = documentai.ProcessRequest(
        name=name,
        raw_document=raw_document
    )
    result = client.process_document(request=request)
    document: documentai.Document = result.document

    elements: List[LayoutElement] = []
    for page in document.pages:
        for block in page.blocks:
            if block.block_type == documentai.Document.Block.BlockType.PARAGRAPH:
                bbox_proto = block.layout.bounding_poly.normalized_vertices
                if bbox_proto:
                    b = BoundingBox(
                        top=bbox_proto[0].y,
                        left=bbox_proto[0].x,
                        width=bbox_proto[2].x - bbox_proto[0].x if len(bbox_proto) > 2 else 0.1,
                        height=bbox_proto[2].y - bbox_proto[0].y if len(bbox_proto) > 2 else 0.1
                    )
                    text = ""  # Build text from token indices in production
                    elements.append(LayoutElement(type="paragraph", bbox=b, text=text))
    return elements
