import os
import json
from typing import Dict, Any, List
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def moderate_vendor_notes(
    vendor_notes: str, memo_fields: List[str] = None
) -> Dict[str, Any]:
    """
    Moderate vendor notes or memo fields using Azure AI Content Safety.

    Args:
        vendor_notes: Text to moderate
        memo_fields: Additional memo fields to check

    Returns:
        Moderation results with safety scores
    """
    # Get Azure Content Safety credentials
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables are required"
        )

    # Create client
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    # Prepare text to analyze
    texts_to_analyze = [vendor_notes]
    if memo_fields:
        texts_to_analyze.extend(memo_fields)

    all_results = []

    for text in texts_to_analyze:
        if not text or not text.strip():
            continue

        # Analyze text with Azure Content Safety
        request = AnalyzeTextOptions(text=text)
        response = client.analyze_text(request)

        # Parse results
        result = {
            "text": text[:100] + "..." if len(text) > 100 else text,
            "hate_result": {
                "category": "Hate",
                "severity": response.hate_result.severity
                if response.hate_result
                else 0,
                "filtered": response.hate_result.severity > 0
                if response.hate_result
                else False,
            },
            "self_harm_result": {
                "category": "SelfHarm",
                "severity": response.self_harm_result.severity
                if response.self_harm_result
                else 0,
                "filtered": response.self_harm_result.severity > 0
                if response.self_harm_result
                else False,
            },
            "sexual_result": {
                "category": "Sexual",
                "severity": response.sexual_result.severity
                if response.sexual_result
                else 0,
                "filtered": response.sexual_result.severity > 0
                if response.sexual_result
                else False,
            },
            "violence_result": {
                "category": "Violence",
                "severity": response.violence_result.severity
                if response.violence_result
                else 0,
                "filtered": response.violence_result.severity > 0
                if response.violence_result
                else False,
            },
        }

        # Determine overall safety
        max_severity = max(
            result["hate_result"]["severity"],
            result["self_harm_result"]["severity"],
            result["sexual_result"]["severity"],
            result["violence_result"]["severity"],
        )

        result["overall_safe"] = max_severity == 0
        result["max_severity"] = max_severity
        result["requires_review"] = max_severity >= 2  # Medium severity or higher

        all_results.append(result)

    # Compile final moderation report
    moderation_report = {
        "provider": "Azure AI Content Safety",
        "endpoint_used": endpoint,
        "texts_analyzed": len(all_results),
        "results": all_results,
        "overall_assessment": "SAFE"
        if all(r["overall_safe"] for r in all_results)
        else "REVIEW_NEEDED",
        "any_high_severity": any(r["max_severity"] >= 3 for r in all_results),
    }

    return moderation_report
