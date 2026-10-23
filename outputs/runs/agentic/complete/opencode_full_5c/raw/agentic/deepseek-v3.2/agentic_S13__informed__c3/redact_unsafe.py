import os
import re
from typing import Tuple, List, Dict, Any
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def redact_unsafe(text: str) -> Tuple[str, List[Dict[str, Any]]]:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Content Safety credentials not configured")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text)
    response = client.analyze_text(request)

    flagged_spans = []
    redacted_text = text

    for category_result in response.categories_analysis:
        if category_result.severity > 0:
            category_name = category_result.category.value

            flagged_spans.append(
                {
                    "category": category_name,
                    "severity": category_result.severity,
                    "text_snippet": text[:50] + "..." if len(text) > 50 else text,
                    "position": 0,
                    "length": len(text),
                }
            )

            if category_name in ["Hate", "SelfHarm", "Sexual", "Violence"]:
                redacted_text = re.sub(r"\b\w+\b", "[REDACTED]", redacted_text)

    return redacted_text, flagged_spans
