import os
import re
from typing import Dict, Any, List, Tuple
from safety_client import get_safety_client


def redact_unsafe(text: str) -> Dict[str, Any]:
    """
    Flags or redacts unsafe spans from text using Azure AI Content Safety.
    """
    client = get_safety_client()

    from azure.ai.contentsafety import ContentSafetyClient
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.contentsafety.models import AnalyzeTextOptions

    if not isinstance(client, ContentSafetyClient):
        raise ValueError("Client must be Azure ContentSafetyClient")

    try:
        request = AnalyzeTextOptions(text=text)
        response = client.analyze_text(request)

        redacted_text = text
        unsafe_spans = []

        if response.categories_analysis:
            for cat_analysis in response.categories_analysis:
                severity = (
                    cat_analysis.severity if hasattr(cat_analysis, "severity") else 0
                )

                if severity >= 2:  # Medium severity or higher
                    category = cat_analysis.category.value

                    words = text.split()
                    for word in words:
                        if (
                            len(word) > 3
                        ):  # Simple heuristic for potentially unsafe words
                            if any(
                                bad in word.lower()
                                for bad in ["hate", "violence", "sexual", "selfharm"]
                            ):
                                unsafe_spans.append(
                                    {
                                        "text": word,
                                        "category": category,
                                        "severity": severity,
                                        "start": text.find(word),
                                        "end": text.find(word) + len(word),
                                    }
                                )

                                # Redact the word
                                redacted_text = redacted_text.replace(
                                    word, "[REDACTED]"
                                )

        return {
            "original": text,
            "redacted": redacted_text,
            "unsafe_spans": unsafe_spans,
            "has_unsafe": len(unsafe_spans) > 0,
        }

    except Exception as e:
        return {
            "original": text,
            "redacted": text,
            "unsafe_spans": [],
            "has_unsafe": False,
            "error": str(e),
        }
