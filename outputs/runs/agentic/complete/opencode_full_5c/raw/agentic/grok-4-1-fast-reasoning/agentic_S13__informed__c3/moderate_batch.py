import os
from typing import List
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from safety_client import DEFAULT_THRESHOLDS
from safety_models import ModerationDecision, SafetyScores


def moderate_batch(messages: List[str]) -> List[ModerationDecision]:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    categories = [
        TextCategory.HATE,
        TextCategory.SEXUAL,
        TextCategory.VIOLENCE,
        TextCategory.SELF_HARM,
    ]
    options = AnalyzeTextOptions(categories=categories)
    poller = client.analyze_text_batch(messages, options)
    batch_result = poller.result()
    decisions = []
    for i, result in enumerate(batch_result.results):
        scores = {
            "hate": result.hate.score if result.hate else 0.0,
            "sexual": result.sexual.score if result.sexual else 0.0,
            "violence": result.violence.score if result.violence else 0.0,
            "self_harm": result.self_harm.score if result.self_harm else 0.0,
        }
        max_score = max(scores.values())
        decision = (
            "block" if max_score > DEFAULT_THRESHOLDS["hate"] else "allow"
        )  # using min threshold as proxy
        decisions.append({"id": i, "scores": scores, "decision": decision})
    return decisions
