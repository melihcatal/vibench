import os
from google.cloud import documentai_v1 as documentai

# Use Document AI Layout processor (identifies blocks, lines, paragraphs, tables, etc.)
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = "us"
PROCESSOR_ID = "projects/{}/locations/{}/processors/{}".format(PROJECT_ID, LOCATION, "document-layout")

def extract_layout_from_image(image_bytes):
    client = documentai.DocumentProcessorServiceClient()
    raw_document = documentai.RawDocument(content=image_bytes, mime_type="image/png")
    input_config = documentai.InputConfig(raw_document=raw_document)
    request = documentai.ProcessRequest(name=PROCESSOR_ID, input_config=input_config)
    result = client.process_document(request=request)
    # Normalize layout elements
    layout = result.document
    elements = []
    for entity in layout.entities:
        elem = {
            "type": entity.type_,
            "text": entity.text_anchor.content if entity.HasField("text_anchor") else "",
            "bounding_poly": [corner for page in entity.bounding_poly.pages for corner in page.vertices]
        }
        elements.append(elem)
    return elements
