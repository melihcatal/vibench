import os
from typing import Dict, Any, List, Tuple
from safety_client import get_content_safety_client


def redact_unsafe(text: str) -> Dict[str, Any]:
    """
    Flag or redact unsafe spans from text using Azure AI Content Safety.
    """
    client = get_content_safety_client()

    from azure.ai.contentsafety import ContentSafetyClient
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

    request = AnalyzeTextOptions(
        text=text,
        categories=[
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE,
        ],
        output_type="EightSeverityLevels",
    )

    response = client.analyze_text(request)

    flagged_spans = []
    redacted_text = text

    for blocklist_result in response.blocklists_match:
        if blocklist_result and blocklist_result.blocklist_name:
            span = {
                "text": blocklist_result.blocklist_item_text,
                "category": "blocklist",
                "severity": 7,
                "offset": blocklist_result.blocklist_item_index,
            }
            flagged_spans.append(span)

            redacted_text = redacted_text.replace(
                blocklist_result.blocklist_item_text, "[REDACTED]"
            )

    for i, char_result in enumerate(response.text_analysis):
        if hasattr(char_result, "severity") and char_result.severity > 0:
            span = {
                "text": text[i],
                "category": char_result.category.value
                if hasattr(char_result, "category")
                else "unknown",
                "severity": char_result.severity,
                "offset": i,
            }
            flagged_spans.append(span)

    if flagged_spans:
        for span in sorted(flagged_spans, key=lambda x: x["offset"], reverse=True):
            if span["severity"] >= 4:
                redacted_text = (
                    redacted_text[: span["offset"]]
                    + "[REDACTED]"
                    + redacted_text[span["offset"] + 1 :]
                )

    return {
        "original_text": text,
        "redacted_text": redacted_text,
        "flagged_spans": flagged_spans,
        "requires_redaction": len(flagged_spans) > 0,
    }
