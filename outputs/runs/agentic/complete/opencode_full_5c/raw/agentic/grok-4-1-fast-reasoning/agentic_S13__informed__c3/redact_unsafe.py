import os
from typing import Dict, List, Any
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import (
    AnalyzeTextDetailedOptions,
    TextCategory,
    SeverityType,
)
from safety_models import RedactResult


def redact_unsafe(text: str) -> RedactResult:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    categories = [
        TextCategory.HATE,
        TextCategory.SEXUAL,
        TextCategory.VIOLENCE,
        TextCategory.SELF_HARM,
    ]
    options = AnalyzeTextDetailedOptions(categories=categories)
    poller = client.analyze_text_detailed(text, options)
    result = poller.result()
    redacted_chars = list(text)
    flags = []
    for loc in sorted(result.locations or [], key=lambda l: l.offset, reverse=True):
        category = loc.category.name.lower()
        severity = loc.severity.name if loc.severity else "NONE"
        start, length = loc.offset, loc.length
        end = start + length
        redacted_chars[start:end] = "*" * length
        flags.append(
            {
                "category": category,
                "severity": severity,
                "offset": start,
                "length": length,
            }
        )
    redacted_text = "".join(redacted_chars)
    return {"redacted_text": redacted_text, "flags": flags, "original_text": text}
