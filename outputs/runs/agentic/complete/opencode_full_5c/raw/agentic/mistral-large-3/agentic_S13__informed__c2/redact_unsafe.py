from typing import Dict, List, Optional, Union
import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import (
    AnalyzeTextOptions,
    TextCategory,
    AnalyzeTextResult,
    TextBlocklistMatch,
)


def redact_unsafe(
    text: str,
    categories: Optional[List[str]] = None,
    block_threshold: Optional[Dict[str, int]] = None,
    custom_blocklists: Optional[List[str]] = None,
) -> Dict[str, Union[str, List[Dict[str, Union[str, int]]]]]:
    """
    Redact unsafe spans from text using Azure AI Content Safety.
    Returns redacted text and detected spans with reasons.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Content Safety credentials not configured")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    if categories is None:
        categories = ["Hate", "SelfHarm", "Sexual", "Violence"]

    azure_categories = {
        "Hate": TextCategory.HATE,
        "SelfHarm": TextCategory.SELF_HARM,
        "Sexual": TextCategory.SEXUAL,
        "Violence": TextCategory.VIOLENCE,
    }

    selected_categories = []
    for cat in categories:
        if cat in azure_categories:
            selected_categories.append(azure_categories[cat])

    if not selected_categories:
        raise ValueError("No valid categories selected")

    request = AnalyzeTextOptions(text=text, categories=selected_categories)
    response: AnalyzeTextResult = client.analyze_text(request)

    scores = {
        "Hate": response.hate_result.severity if response.hate_result else 0,
        "SelfHarm": response.self_harm_result.severity
        if response.self_harm_result
        else 0,
        "Sexual": response.sexual_result.severity if response.sexual_result else 0,
        "Violence": response.violence_result.severity
        if response.violence_result
        else 0,
    }

    decision = False
    if block_threshold:
        decision = any(
            scores.get(cat, 0) >= threshold
            for cat, threshold in block_threshold.items()
            if cat in scores
        )

    detected_spans = []
    redacted_text = text
    offset = 0

    if response.hate_result and response.hate_result.severity > 0:
        for item in response.hate_result.detected_text_items or []:
            start = item.start_index
            end = item.end_index
            detected_spans.append(
                {
                    "text": text[start:end],
                    "category": "Hate",
                    "severity": response.hate_result.severity,
                    "start_index": start,
                    "end_index": end,
                }
            )
            redacted_text = (
                redacted_text[: start + offset]
                + "[REDACTED]"
                + redacted_text[end + offset :]
            )
            offset += len("[REDACTED]") - (end - start)

    if response.self_harm_result and response.self_harm_result.severity > 0:
        for item in response.self_harm_result.detected_text_items or []:
            start = item.start_index
            end = item.end_index
            detected_spans.append(
                {
                    "text": text[start:end],
                    "category": "SelfHarm",
                    "severity": response.self_harm_result.severity,
                    "start_index": start,
                    "end_index": end,
                }
            )
            redacted_text = (
                redacted_text[: start + offset]
                + "[REDACTED]"
                + redacted_text[end + offset :]
            )
            offset += len("[REDACTED]") - (end - start)

    if response.sexual_result and response.sexual_result.severity > 0:
        for item in response.sexual_result.detected_text_items or []:
            start = item.start_index
            end = item.end_index
            detected_spans.append(
                {
                    "text": text[start:end],
                    "category": "Sexual",
                    "severity": response.sexual_result.severity,
                    "start_index": start,
                    "end_index": end,
                }
            )
            redacted_text = (
                redacted_text[: start + offset]
                + "[REDACTED]"
                + redacted_text[end + offset :]
            )
            offset += len("[REDACTED]") - (end - start)

    if response.violence_result and response.violence_result.severity > 0:
        for item in response.violence_result.detected_text_items or []:
            start = item.start_index
            end = item.end_index
            detected_spans.append(
                {
                    "text": text[start:end],
                    "category": "Violence",
                    "severity": response.violence_result.severity,
                    "start_index": start,
                    "end_index": end,
                }
            )
            redacted_text = (
                redacted_text[: start + offset]
                + "[REDACTED]"
                + redacted_text[end + offset :]
            )
            offset += len("[REDACTED]") - (end - start)

    if custom_blocklists:
        for blocklist_name in custom_blocklists:
            matches = client.analyze_text_with_blocklist(
                text=text,
                blocklist_names=[blocklist_name],
            )
            for match in matches.blocklists_match_results or []:
                for item in match.detected_text_items or []:
                    start = item.start_index
                    end = item.end_index
                    detected_spans.append(
                        {
                            "text": text[start:end],
                            "category": "Blocklist",
                            "blocklist_name": blocklist_name,
                            "severity": 6,  # Max severity for blocklist matches
                            "start_index": start,
                            "end_index": end,
                        }
                    )
                    redacted_text = (
                        redacted_text[: start + offset]
                        + "[REDACTED]"
                        + redacted_text[end + offset :]
                    )
                    offset += len("[REDACTED]") - (end - start)

    return {
        "redacted_text": redacted_text,
        "detected_spans": detected_spans,
        "decision": decision,
    }
