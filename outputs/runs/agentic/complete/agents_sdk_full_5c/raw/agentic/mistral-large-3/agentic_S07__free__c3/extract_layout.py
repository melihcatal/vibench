import os
from typing import Dict, Any, List
import requests
from document_client import get_document_client
from document_models import LayoutExtractionResponse, LayoutBlock


def extract_layout(image_path: str) -> LayoutExtractionResponse:
    """
    Extract layout elements (blocks, lines, paragraphs) from a document using Google Cloud Vision API.
    """
    client = get_document_client()
    
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    
    # Google Cloud Vision API-specific request for document text detection
    request_payload = {
        "requests": [
            {
                "image": {"content": content},
                "features": [{"type": "DOCUMENT_TEXT_DETECTION"}],
                "imageContext": {"languageHints": ["en"]}
            }
        ]
    }
    
    response = requests.post(
        f"https://vision.googleapis.com/v1/images:annotate?key={os.getenv('GOOGLE_CLOUD_VISION_API_KEY')}",
        json=request_payload
    )
    response.raise_for_status()
    
    result = response.json()
    blocks = []
    
    if "fullTextAnnotation" in result["responses"][0]:
        for page in result["responses"][0]["fullTextAnnotation"].get("pages", []):
            for block in page.get("blocks", []):
                block_text = "".join([
                    paragraph.get("text", "")
                    for paragraph in block.get("paragraphs", [])
                ])
                blocks.append(
                    LayoutBlock(
                        block_type=block.get("blockType", "UNKNOWN"),
                        text=block_text,
                        bounding_box=block.get("boundingBox", {}).get("vertices", []),
                        confidence=block.get("confidence", 0.0)
                    )
                )
    
    return LayoutExtractionResponse(
        blocks=blocks,
        provider="google_cloud_vision",
        raw_response=result
    )