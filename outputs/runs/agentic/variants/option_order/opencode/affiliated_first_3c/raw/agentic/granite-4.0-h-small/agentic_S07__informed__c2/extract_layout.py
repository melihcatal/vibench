import os
import json
from document_client import OcrClient


def extract_layout(image_path: str) -> dict:
    """Extract document blocks, lines, tables, or layout elements from an image.

    Uses Azure AI Document Intelligence as the concrete provider. Set the environment variables AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY.
    """
    client = OcrClient()  # Azure Document Intelligence SDK client
    response = client.begin_analyze_document("Layout", image_path)
    result = response.result()
    # Convert Azure layout output to a generic layout dict
    layout = {
        "blocks": [b.as_dict() for b in result.layout.blocks],
        "lines": [l.as_dict() for l in result.layout.lines],
        "tables": [t.as_dict() for t in result.layout.tables],
    }
    return layout
