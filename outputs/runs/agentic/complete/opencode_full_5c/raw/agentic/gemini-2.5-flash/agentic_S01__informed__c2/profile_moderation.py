from identity_client import AzureContentSafetyClient
from identity_models import (
    ModerateProfileRequest,
    ModerateProfileResponse,
    ModerationResult,
)
from azure.ai.contentsafety.models import AnalyzeTextOptions


def profile_moderation(request: ModerateProfileRequest) -> ModerateProfileResponse:
    client = AzureContentSafetyClient()
    text_safety_input = AnalyzeTextOptions(text=request.text)
    response = client.client.analyze_text(text_safety_input)

    is_safe = True
    results = []
    if response.categories_analysis:
        for category_analysis in response.categories_analysis:
            results.append(
                ModerationResult(
                    category=category_analysis.category.value,
                    severity=category_analysis.severity,
                )
            )
            if category_analysis.severity > 0:  # Assuming severity > 0 means unsafe
                is_safe = False

    return ModerateProfileResponse(is_safe=is_safe, results=results)
