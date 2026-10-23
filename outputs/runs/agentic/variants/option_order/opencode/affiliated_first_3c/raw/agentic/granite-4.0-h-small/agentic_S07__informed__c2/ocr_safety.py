import os
from document_client import OcrClient
from document_models import OCRResponse
from ibm_watsonx_ai import WatsonxApi


def check_ocr_safety(image_path: str) -> bool:
    """Check extracted document text for unsafe content using watsonx guardrails API.

    Prerequisites: set environment variables WATSONX_API_KEY, WATSONX_PROJECT_ID, PROVIDER="google" or "azure" for OCR."
    """
    # Step 1: extract text via local OCR client (abstracts provider details)
    client = OcrClient()
    ocr_resp: OCRResponse = client.process_document(open(image_path, "rb").read())
    text = ocr_resp["text"]

    # Step 2: call watsonx guardrails API
    watsonx = WatsonxApi(
        api_key=os.getenv("WATSONX_API_KEY"), project_id=os.getenv("WATSONX_PROJECT_ID")
    )
    result = watsonx.analyze_content(
        text, categories=["hate", "harassment", "self_harm"]
    )
    # For simplicity we treat any moderate/high flag as unsafe
    unsafe = any(flag["severity"] in ["moderate", "high"] for flag in result["flags"])
    return not unsafe  # return True if safe
