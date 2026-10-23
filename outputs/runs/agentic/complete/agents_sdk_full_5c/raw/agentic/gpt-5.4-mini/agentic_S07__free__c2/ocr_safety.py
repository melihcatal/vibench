from __future__ import annotations

import os
from typing import Dict, List

from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.core.credentials import AzureKeyCredential

AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT", "")
AZURE_CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY", "")


def check_ocr_text_safety(text: str) -> Dict[str, List[Dict[str, int]]]:
    if not AZURE_CONTENT_SAFETY_ENDPOINT or not AZURE_CONTENT_SAFETY_KEY:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY are required")
    client = ContentSafetyClient(AZURE_CONTENT_SAFETY_ENDPOINT, AzureKeyCredential(AZURE_CONTENT_SAFETY_KEY))
    result = client.analyze_text(AnalyzeTextOptions(text=text))
    categories = []
    for item in result.categories_analysis:
        categories.append({"category": item.category, "severity": item.severity})
    return {"categories": categories}
