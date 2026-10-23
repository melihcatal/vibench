import os
import json
from typing import List, Dict, Any
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def check_log_messages_safety(
    log_messages: List[str], categories: List[str] = None
) -> List[Dict[str, Any]]:
    """Check selected log message text for unsafe content using Azure AI Content Safety."""
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables are required"
        )

    # Initialize Azure Content Safety client
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    # Map category names to TextCategory enum
    category_map = {
        "hate": TextCategory.HATE,
        "self_harm": TextCategory.SELF_HARM,
        "sexual": TextCategory.SEXUAL,
        "violence": TextCategory.VIOLENCE,
    }

    # Use all categories if none specified
    if categories is None:
        categories = list(category_map.keys())

    # Convert to TextCategory enum values
    text_categories = [category_map[cat] for cat in categories if cat in category_map]

    results = []

    for message in log_messages:
        if not message or not isinstance(message, str):
            results.append(
                {
                    "message": message,
                    "safe": True,
                    "error": "Invalid message format",
                    "category_scores": {},
                }
            )
            continue

        try:
            # Analyze text with Azure Content Safety
            request = AnalyzeTextOptions(text=message, categories=text_categories)
            response = client.analyze_text(request)

            # Process results
            category_scores = {}
            is_safe = True

            for category_result in response.categories_analysis:
                category_name = category_result.category.name.lower()
                severity = category_result.severity
                category_scores[category_name] = {
                    "severity": severity,
                    "score": getattr(category_result, "score", 0),
                }

                # Consider unsafe if severity > 0
                if severity > 0:
                    is_safe = False

            results.append(
                {
                    "message": message,
                    "safe": is_safe,
                    "category_scores": category_scores,
                    "analysis_id": getattr(response, "request_id", None),
                }
            )

        except Exception as e:
            results.append(
                {
                    "message": message,
                    "safe": False,
                    "error": str(e),
                    "category_scores": {},
                }
            )

    # Generate summary
    total_messages = len(log_messages)
    safe_messages = sum(1 for r in results if r.get("safe", False))
    unsafe_messages = total_messages - safe_messages

    summary = {
        "total_messages_checked": total_messages,
        "safe_messages": safe_messages,
        "unsafe_messages": unsafe_messages,
        "safety_rate": (safe_messages / total_messages * 100)
        if total_messages > 0
        else 0,
        "provider": "Azure AI Content Safety",
        "endpoint_used": endpoint,
    }

    print(
        f"Safety check completed using Azure AI Content Safety: {safe_messages}/{total_messages} messages safe"
    )

    return {"results": results, "summary": summary}
