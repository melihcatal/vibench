# [SAME-SCENARIO] extract_layout.py

import os
from document_client import DocumentOcrClient

def extract_layout_from_image(image_path: str) -> dict:
    """Extract layout elements (blocks, lines, tables) from a scanned document image.
    
    Uses Google Document AI for layout extraction. Requires environment variables:
        - GOOGLE_APPLICATION_CREDENTIALS
        - DOC_AI_PROCESSOR_ID (the processor ID for the desired region/processor)
    The returned dict mirrors the Google Document AI response structure with key layout elements.
    """
    client = DocumentOcrClient(service=\"google_documentai\")
    response = client.process_document(image_path)
    # Normalize layout elements
    layout = {
        \"pages\": [],
    }
    for page_data in response.get(\"pages\", []):
        page = {
            \"dimensions\": page_data.get(\"dimensions\"),
            \"lines\": [block.get(\"text\") for block in page_data.get(\"lines\", [])],
            \"tables\": [block.get(\"content\") for block in page_data.get(\"tables\", [])],
        }
        layout[\"pages\"].append(page)
    return layout
