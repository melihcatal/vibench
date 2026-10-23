from typing import List
from azure.ai.contentsafety.models import AnalyzeTextOptions
from safety_client import get_safety_client
from safety_models import BatchModerationRequest, ModerationResponse, CategoryScore


def moderate_batch(request: BatchModerationRequest) -> List[ModerationResponse]:
    client = get_safety_client()
    results = []

    for text_item in request.texts:
        analysis_request = AnalyzeTextOptions(text=text_item)
        response = client.analyze_text(analysis_request)

        scores = []
        if response.hate_result:
            scores.append(
                CategoryScore(category="Hate", severity=response.hate_result.severity)
            )
        if response.self_harm_result:
            scores.append(
                CategoryScore(
                    category="SelfHarm", severity=response.self_harm_result.severity
                )
            )
        if response.sexual_result:
            scores.append(
                CategoryScore(
                    category="Sexual", severity=response.sexual_result.severity
                )
            )
        if response.violence_result:
            scores.append(
                CategoryScore(
                    category="Violence", severity=response.violence_result.severity
                )
            )

        results.append(ModerationResponse(text=text_item, scores=scores))

    return results
