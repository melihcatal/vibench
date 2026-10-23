# extract_layout.py
# SAME-SCENARIO OCR file
# Uses Google Document AI via google-cloud-documentai SDK

import os
from google.cloud import documentai_v1 as documentai

# Use GOOGLE_APPLICATION_CREDENTIALS environment variable for auth
client = documentai.DocumentProcessorServiceClient()


def extract_layout_from_image(image_path: str):
    """Extract blocks, lines, and tables from a document image using Google Document AI.

    Args:
        image_path: Local path to the image file.

    Returns:
        A list of layout elements with type and content.
    """
    # Load image
    with open(image_path, "rb") as f:
        image_content = f.read()

    # Prepare request
    name = "projects/PROJECT_ID/locations/LOCATION/processors/PROCESSOR_ID"
    document = documentai.Document(content=image_content, mime_type="image/png")
    request = documentai.ProcessRequest(name=name, document=document)

    # Process document
    response = client.process_document(request=request)
    layout_elements = []
    for token in response.document.tokens:
        layout_elements.append({"type": "token", "text": token.text})
    # Additional extraction for blocks, lines, and tables can be added here
    return layout_elements
