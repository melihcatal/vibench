from model_client import LLMClientFactory
from model_models import SafetyCheckRequest, SafetyCheckResult
from azure.ai.contentsafety.models import TextContent, AnalyzeTextOptions, TextCategory
import os

def check_prompt_safety(request: SafetyCheckRequest) -> SafetyCheckResult:
    client = LLMClientFactory.get_azure_content_safety_client()

    categories = [
        TextCategory.HATE,
        TextCategory.SELF_HARM,
        TextCategory.SEXUAL,
        TextCategory.VIOLENCE,
    ]

    BLOCK_THRESHOLD = 4

    response = client.analyze_text(
        AnalyzeTextOptions(
            text=TextContent(text=request.text),
            categories=categories,
            blocklist_names=[],
            output_type="FourPoint"
        )
    )

    is_safe = True
    reasons = []

    for category_result in response.categories_analysis:
        if category_result.severity >= BLOCK_THRESHOLD:
            is_safe = False
            reasons.append(f"{category_result.category.name} (Severity: {category_result.severity})")

    return SafetyCheckResult(safe=is_safe, reasons=reasons)