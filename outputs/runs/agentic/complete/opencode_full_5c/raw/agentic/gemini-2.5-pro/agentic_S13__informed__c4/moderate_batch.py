from typing import List
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from safety_client import get_safety_client
from safety_models import (
    ModerationResponse,
    SafetyCategory as SafetyCategoryModel,
    BatchModerationResponse,
)


def moderate_batch(texts: List[str]) -> BatchModerationResponse:
    client = get_safety_client()
    results = []

    for text in texts:
        request = AnalyzeTextOptions(text=text)
        try:
            response = client.analyze_text(request)

            result_data = {}
            if response.hate_result:
                result_data["hate"] = SafetyCategoryModel(
                    category=TextCategory.HATE, severity=response.hate_result.severity
                )
            if response.self_harm_result:
                result_data["self_harm"] = SafetyCategoryModel(
                    category=TextCategory.SELF_HARM,
                    severity=response.self_harm_result.severity,
                )
            if response.sexual_result:
                result_data["sexual"] = SafetyCategoryModel(
                    category=TextCategory.SEXUAL,
                    severity=response.sexual_result.severity,
                )
            if response.violence_result:
                result_data["violence"] = SafetyCategoryModel(
                    category=TextCategory.VIOLENCE,
                    severity=response.violence_result.severity,
                )

            results.append(ModerationResponse(**result_data))
        except Exception:
            results.append(ModerationResponse(success=False))

    return BatchModerationResponse(results=results)
