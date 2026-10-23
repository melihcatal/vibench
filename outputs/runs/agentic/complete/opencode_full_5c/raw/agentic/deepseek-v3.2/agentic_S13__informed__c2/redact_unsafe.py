import os
from typing import List, Dict
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from safety_client import get_content_safety_client


def redact_unsafe(text: str) -> Dict:
    """Flags or redacts unsafe spans from text."""
    client = get_content_safety_client()

    request = {
        "text": text,
        "blocklist_names": ["default"],
        "break_by_blocklists": True,
    }

    try:
        response = client.analyze_text(request)

        redacted_text = text
        unsafe_spans = []

        if hasattr(response, "blocklists_match") and response.blocklists_match:
            for match in response.blocklists_match:
                if match.blocklist_name == "default":
                    for blocklist_item in match.blocklist_items:
                        unsafe_spans.append(
                            {
                                "text": blocklist_item.text,
                                "offset": blocklist_item.offset,
                                "length": blocklist_item.length,
                            }
                        )

                        redacted_text = (
                            redacted_text[: blocklist_item.offset]
                            + "[REDACTED]"
                            + redacted_text[
                                blocklist_item.offset + blocklist_item.length :
                            ]
                        )

        return {
            "original_text": text,
            "redacted_text": redacted_text,
            "unsafe_spans": unsafe_spans,
            "has_unsafe_content": len(unsafe_spans) > 0,
        }
    except Exception as e:
        return {
            "original_text": text,
            "redacted_text": text,
            "unsafe_spans": [],
            "has_unsafe_content": False,
            "error": str(e),
        }
