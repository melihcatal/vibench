import os
import dashscope
from vision_client import VisionClient
from vision_models import DescriptionRequest, DescriptionResponse
from typing import List

# Explicit provider identifier for later‑step LLM inference
PROVIDER = "DashScope"


def image_summary(analysis_results: List[dict]) -> str:
    """Summarize visual analysis results (labels, description, text, safety) using a DashScope Qwen model.
    Returns a concise summary paragraph.
    """
    client = VisionClient()
    # Build a prompt that includes the extracted data
    prompt = (
        "Summarize the following visual analysis in one short paragraph."
        f"\nLabels: {analysis_results.get('labels', [])}"
        f"\nDescription: {analysis_results.get('description', '')}"
        f"\nExtracted Text: {analysis_results.get('text', '')}"
        f"\nSafety: {analysis_results.get('safe', True)}"
    )
    request = DescriptionRequest(image_path=None, instruction=prompt)
    raw = client.description(request)
    return raw["description"].strip()
