from safety_client import get_content_safety_client
from safety_models import ModerationResult, ModerationCategory
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def moderate_text(text: str) -> ModerationResult:
    client = get_content_safety_client()
    request = AnalyzeTextOptions(text=text)
    response = client.analyze_text(request)

    categories = []
    for result in response.categories_analysis:
        category_name = result.category.value
        severity = result.severity
        detected = severity > 0  # Assuming severity > 0 means detected
        categories.append(
            ModerationCategory(
                category=category_name, severity=severity, detected=detected
            )
        )

    return ModerationResult(text=text, categories=categories)
