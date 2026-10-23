import os
from typing import Dict, Any, List
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import TextCategory
from safety_models import SafetyResult


def moderate_text(text: str) -> SafetyResult:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError("Azure Content Safety credentials missing")
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    poller = client.analyze_text(
        text=text,
        categories=[
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE,
            TextCategory.HARASSMENT,
        ],
    )
    result = poller.result()
    categories: Dict[str, float] = {}
    blocked_reasons: List[str] = []
    for cat_result in getattr(result, "categories_results", []):
        cat_name = (
            cat_result.category.value.lower()
            if hasattr(cat_result.category, "value")
            else ""
        )
        severity = getattr(cat_result, "severity", None)
        score = severity.value / 4.0 if severity and hasattr(severity, "value") else 0.0
        categories[cat_name] = score
        if score > 0.5:
            blocked_reasons.append(cat_name)
    overall_blocked = bool(blocked_reasons)
    rationale = (
        f"Blocked categories: {', '.join(blocked_reasons)}"
        if blocked_reasons
        else "Passed all checks"
    )
    return {
        "categories": categories,
        "overall_blocked": overall_blocked,
        "rationale": rationale,
        "redacted_text": "",
        "flagged_spans": [],
        "raw_response": vars(result),
    }
