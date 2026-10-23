import os
from typing import Dict, Any, List
import requests
from document_client import get_document_client
from document_models import LayoutExtractionResponse, LayoutBlock


def extract_layout(image_path: str) -> LayoutExtractionResponse:
    """
    Extract layout elements (blocks, lines, paragraphs) from a document using Azure Form Recognizer.
    """
    endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
    key = os.getenv("AZURE_FORM_RECOGNIZER_KEY")
    
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    
    # Azure Form Recognizer-specific request for layout analysis
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/octet-stream"
    }
    
    response = requests.post(
        f"{endpoint}/formrecognizer/documentModels/prebuilt-layout:analyze?readingOrder=natural",
        headers=headers,
        data=content
    )
    response.raise_for_status()
    
    operation_url = response.headers["Operation-Location"]
    result = _poll_azure_operation(operation_url, headers)
    
    blocks = []
    for page in result.get("analyzeResult", {}).get("pages", []):
        for block in page.get("paragraphs", []):
            blocks.append(
                LayoutBlock(
                    text=block.get("content", ""),
                    bounding_box=block.get("polygon", []),
                    block_type="paragraph"
                )
            )
        for block in page.get("lines", []):
            blocks.append(
                LayoutBlock(
                    text=block.get("content", ""),
                    bounding_box=block.get("polygon", []),
                    block_type="line"
                )
            )
    
    return LayoutExtractionResponse(
        blocks=blocks,
        provider="azure_form_recognizer",
        raw_response=result
    )


def _poll_azure_operation(operation_url: str, headers: Dict[str, str]) -> Dict[str, Any]:
    """Poll Azure Form Recognizer operation until completion."""
    while True:
        response = requests.get(operation_url, headers=headers)
        response.raise_for_status()
        result = response.json()
        if result.get("status") in ["succeeded", "failed"]:
            return result
        import time
        time.sleep(2)