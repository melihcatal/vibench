import os
from typing import Dict, Any, Optional
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory, RedactTextOptions


def redact_unsafe(text: str, category_thresholds: Dict[str, int]) -> Dict[str, Any]:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Content Safety endpoint and key must be set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    # Analyze text for unsafe content
    analyze_request = AnalyzeTextOptions(
        text=text,
        categories=[
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE
        ],
        output_type="EightSeverityLevels"
    )
    analyze_response = client.analyze_text(analyze_request)

    # Determine if redaction is needed
    needs_redaction = (
        (analyze_response.hate_result.severity if analyze_response.hate_result else 0) >= category_thresholds.get("hate", 0) or
        (analyze_response.self_harm_result.severity if analyze_response.self_harm_result else 0) >= category_thresholds.get("self_harm", 0) or
        (analyze_response.sexual_result.severity if analyze_response.sexual_result else 0) >= category_thresholds.get("sexual", 0) or
        (analyze_response.violence_result.severity if analyze_response.violence_result else 0) >= category_thresholds.get("violence", 0)
    )

    redacted_text = text
    if needs_redaction:
        redact_request = RedactTextOptions(
            text=text,
            categories=[
                TextCategory.HATE,
                TextCategory.SELF_HARM,
                TextCategory.SEXUAL,
                TextCategory.VIOLENCE
            ]
        )
        redact_response = client.redact_text(redact_request)
        redacted_text = redact_response.redacted_text

    return {
        "redacted_text": redacted_text,
        "hate": analyze_response.hate_result.severity if analyze_response.hate_result else 0,
        "self_harm": analyze_response.self_harm_result.severity if analyze_response.self_harm_result else 0,
        "sexual": analyze_response.sexual_result.severity if analyze_response.sexual_result else 0,
        "violence": analyze_response.violence_result.severity if analyze_response.violence_result else 0
    }