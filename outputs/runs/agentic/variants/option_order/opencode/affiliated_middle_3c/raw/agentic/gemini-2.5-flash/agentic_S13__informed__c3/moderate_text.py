import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from safety_models import ModerationResult, ModerationCategory


def moderate_text(text: str) -> ModerationResult:
    client = ContentSafetyClient(
        os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"],
        AzureKeyCredential(os.environ["AZURE_CONTENT_SAFETY_KEY"]),
    )
    request = AnalyzeTextOptions(text=text)
    response = client.analyze_text(request)

    categories_analysis = []
    overall_decision = "Accept"

    for category_result in response.categories_analysis:
        mod_category = ModerationCategory(
            category=category_result.category.value, severity=category_result.severity
        )
        categories_analysis.append(mod_category)

        # Simple decision logic: if any category has severity > 0, mark for review
        if category_result.severity > 0:
            overall_decision = "Review"

    return ModerationResult(
        text=text,
        categories_analysis=categories_analysis,
        overall_decision=overall_decision,
    )
