# stored_asset_summary.py
# [LATER-STEP] Summarize content extracted from a stored asset using Granite (watsonx.ai) SDK

import os
import ibm_watsonx_ai as watsonx
from ibm_watsonx_ai.llm import GraniteChatRequest
from storage_models import OCRResult


def summarize_asset(
    ocr_result: OCRResult, model_id: str = "granite-4.0-h-small"
) -> str:
    """Generates a concise summary of OCR text using Granite via watsonx.ai.
    Args:
        ocr_result (OCRResult): Object containing extracted text and optional boxes.
        model_id (str): Granite model identifier (default matches provided list).
    Returns:
        str: Human-readable summary.
    """
    # Initialize Granite client (uses environment variables WATSONX_API_KEY, WATSONX_PROJECT_ID)
    client = watsonx.Watsonx()  # Handles auth via env vars
    # Construct prompt for summarization
    prompt = f"Summarize the following document in three sentences, preserving key information:\n\n{ocr_result.text}"
    request = GraniteChatRequest(prompt=prompt, model=model_id)
    response = client.chat_completion(request)
    return response.message.content.strip()


# Example usage (uncomment and ensure credentials are set)
# ocr = OCRResult(text="This is a long document about the history of space exploration...")
# summary = summarize_asset(ocr)
# print('Summary:', summary)
