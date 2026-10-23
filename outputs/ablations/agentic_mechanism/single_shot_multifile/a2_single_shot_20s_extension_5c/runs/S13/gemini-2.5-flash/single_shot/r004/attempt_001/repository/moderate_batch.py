from typing import List
import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextContent
from azure.core.credentials import AzureKeyCredential

from safety_models import BatchModerationRequest, BatchModerationResponse, ModerationResult, ModerationScore, HarmCategory

def moderate_batch(batch_request: BatchModerationRequest) -> BatchModerationResponse:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    results: List[ModerationResult] = []

    for text_to_moderate in batch_request.texts:
        request = AnalyzeTextOptions(text=text_to_moderate)
        try:
            response = client.analyze_text(request)
            scores: List[ModerationScore] = []
            
            if response.hate_result:
                scores.append(ModerationScore(category=HarmCategory.HATE_SPEECH, score=response.hate_result.severity / 7.0))
            if response.self_harm_result:
                scores.append(ModerationScore(category=HarmCategory.DANGEROUS_CONTENT, score=response.self_harm_result.severity / 7.0))
            if response.sexual_result:
                scores.append(ModerationScore(category=HarmCategory.SEXUAL, score=response.sexual_result.severity / 7.0))
            if response.violence_result:
                scores.append(ModerationScore(category=HarmCategory.VIOLENCE, score=response.violence_result.severity / 7.0))

            results.append(ModerationResult(text=text_to_moderate, scores=scores, decision="SCORED"))
        except Exception as e:
            results.append(ModerationResult(text=text_to_moderate, scores=[], decision=f"ERROR: {e}"))

    return BatchModerationResponse(results=results)