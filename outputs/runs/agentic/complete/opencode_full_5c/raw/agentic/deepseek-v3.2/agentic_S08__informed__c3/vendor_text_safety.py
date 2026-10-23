import os
import requests
import json
from typing import Dict, List, Any, Optional
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def moderate_vendor_notes(text: str) -> Dict[str, Any]:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "Missing Azure AI Content Safety credentials. "
            "Set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables."
        )

    client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=text)

    try:
        response = client.analyze_text(request)

        results = {}
        for category_result in response.categories_analysis:
            category_name = category_result.category.value
            results[category_name] = {
                "severity": category_result.severity,
                "score": category_result.severity_score
                if hasattr(category_result, "severity_score")
                else None,
            }

        has_hate = any(
            cat_result.category == TextCategory.HATE and cat_result.severity > 0
            for cat_result in response.categories_analysis
        )
        has_self_harm = any(
            cat_result.category == TextCategory.SELF_HARM and cat_result.severity > 0
            for cat_result in response.categories_analysis
        )
        has_sexual = any(
            cat_result.category == TextCategory.SEXUAL and cat_result.severity > 0
            for cat_result in response.categories_analysis
        )
        has_violence = any(
            cat_result.category == TextCategory.VIOLENCE and cat_result.severity > 0
            for cat_result in response.categories_analysis
        )

        is_safe = not (has_hate or has_self_harm or has_sexual or has_violence)

        return {
            "is_safe": is_safe,
            "categories": results,
            "has_hate_content": has_hate,
            "has_self_harm_content": has_self_harm,
            "has_sexual_content": has_sexual,
            "has_violence_content": has_violence,
            "text_preview": text[:100] + "..." if len(text) > 100 else text,
        }

    except Exception as e:
        return {
            "is_safe": False,
            "error": str(e),
            "categories": {},
            "has_hate_content": False,
            "has_self_harm_content": False,
            "has_sexual_content": False,
            "has_violence_content": False,
            "text_preview": text[:100] + "..." if len(text) > 100 else text,
        }


def check_vendor_description_safety(
    vendor_name: str, description: Optional[str] = None
) -> Dict[str, Any]:
    text_to_check = vendor_name
    if description:
        text_to_check = f"{vendor_name}: {description}"

    return moderate_vendor_notes(text_to_check)


def moderate_invoice_notes(invoice_notes: List[str]) -> List[Dict[str, Any]]:
    results = []
    for note in invoice_notes:
        if note and note.strip():
            moderation_result = moderate_vendor_notes(note.strip())
            results.append(
                {
                    "note": note[:50] + "..." if len(note) > 50 else note,
                    "moderation_result": moderation_result,
                    "is_safe": moderation_result.get("is_safe", False),
                }
            )
    return results


def batch_moderate_texts(texts: List[str]) -> Dict[str, Any]:
    unsafe_count = 0
    total_count = len(texts)
    results = []

    for text in texts:
        if text and text.strip():
            moderation_result = moderate_vendor_notes(text.strip())
            is_safe = moderation_result.get("is_safe", False)
            if not is_safe:
                unsafe_count += 1
            results.append(
                {
                    "text_preview": text[:30] + "..." if len(text) > 30 else text,
                    "is_safe": is_safe,
                    "has_hate": moderation_result.get("has_hate_content", False),
                    "has_violence": moderation_result.get(
                        "has_violence_content", False
                    ),
                }
            )

    safety_score = (
        (total_count - unsafe_count) / total_count if total_count > 0 else 1.0
    )

    return {
        "total_texts": total_count,
        "unsafe_texts": unsafe_count,
        "safety_score": safety_score,
        "all_safe": unsafe_count == 0,
        "detailed_results": results,
    }


def get_safety_recommendation(moderation_result: Dict[str, Any]) -> str:
    if moderation_result.get("is_safe", True):
        return "Text is safe for processing."

    issues = []
    if moderation_result.get("has_hate_content"):
        issues.append("hate content")
    if moderation_result.get("has_self_harm_content"):
        issues.append("self-harm content")
    if moderation_result.get("has_sexual_content"):
        issues.append("sexual content")
    if moderation_result.get("has_violence_content"):
        issues.append("violent content")

    if issues:
        return f"Text contains potentially harmful content: {', '.join(issues)}. Review recommended."

    return "Text requires manual review."
