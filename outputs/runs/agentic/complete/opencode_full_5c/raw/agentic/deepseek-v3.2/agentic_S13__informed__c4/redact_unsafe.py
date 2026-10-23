import os
from typing import List, Tuple
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential


def redact_unsafe(text: str) -> Tuple[str, List[Dict]]:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Content Safety credentials not configured")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = {
        "text": text,
        "blocklist_names": ["default"],
        "halt_on_blocklist_hit": False,
    }

    response = client.analyze_text(request)

    redacted_text = text
    flagged_spans = []

    if hasattr(response, "blocklists_match") and response.blocklists_match:
        for match in response.blocklists_match:
            flagged_spans.append(
                {
                    "text": match.blocklist_item_text,
                    "offset": match.offset,
                    "length": match.length,
                }
            )

    if hasattr(response, "text_analysis") and response.text_analysis:
        for analysis in response.text_analysis:
            if analysis.severity >= 2:
                flagged_spans.append(
                    {
                        "text": text[
                            analysis.offset : analysis.offset + analysis.length
                        ],
                        "offset": analysis.offset,
                        "length": analysis.length,
                        "category": analysis.category,
                        "severity": analysis.severity,
                    }
                )

    flagged_spans.sort(key=lambda x: x["offset"], reverse=True)

    for span in flagged_spans:
        redacted_text = (
            redacted_text[: span["offset"]]
            + "[REDACTED]"
            + redacted_text[span["offset"] + span["length"] :]
        )

    return redacted_text, flagged_spans
