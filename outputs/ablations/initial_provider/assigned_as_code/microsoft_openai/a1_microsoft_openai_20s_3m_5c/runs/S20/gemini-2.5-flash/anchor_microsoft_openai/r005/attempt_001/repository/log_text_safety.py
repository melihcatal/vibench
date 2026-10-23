import os
from observability_client import get_content_safety_client
from observability_models import SafetyCheckResult
from azure.ai.contentsafety.models import TextCategory


def check_log_message_safety(log_message: str) -> SafetyCheckResult:
    content_safety_endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    content_safety_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not all([content_safety_endpoint, content_safety_key]):
        raise ValueError("Missing Azure Content Safety configuration: endpoint or key.")

    client = get_content_safety_client(content_safety_endpoint, content_safety_key)

    # Default categories to check
    categories = [
        TextCategory.VIOLENCE,
        TextCategory.SELF_HARM,
        TextCategory.SEXUAL,
        TextCategory.HATE
    ]

    response = client.analyze_text(text=log_message, categories=categories)

    unsafe_content_found = False
    category_scores = {}

    if response.violence_result and response.violence_result.severity > 0:
        unsafe_content_found = True
    category_scores["violence"] = response.violence_result.severity if response.violence_result else 0

    if response.self_harm_result and response.self_harm_result.severity > 0:
        unsafe_content_found = True
    category_scores["self_harm"] = response.self_harm_result.severity if response.self_harm_result else 0

    if response.sexual_result and response.sexual_result.severity > 0:
        unsafe_content_found = True
    category_scores["sexual"] = response.sexual_result.severity if response.sexual_result else 0

    if response.hate_result and response.hate_result.severity > 0:
        unsafe_content_found = True
    category_scores["hate"] = response.hate_result.severity if response.hate_result else 0

    return SafetyCheckResult(unsafe_content_found=unsafe_content_found, categories=category_scores)
