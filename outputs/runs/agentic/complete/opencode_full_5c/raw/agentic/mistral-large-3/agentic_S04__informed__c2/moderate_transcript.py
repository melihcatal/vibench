import os
from typing import List, Dict, Any
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import TextAnalyzeInput, AnalyzeTextOptions


def moderate_transcript(segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError("Azure Content Safety credentials not set")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    moderated_segments = []

    for segment in segments:
        input_text = TextAnalyzeInput(
            text=segment["text"],
            analyze_text_options=AnalyzeTextOptions(
                categories=["Hate", "SelfHarm", "Sexual", "Violence"]
            ),
        )
        response = client.analyze_text(input_text)
        moderated_segments.append(
            {
                **segment,
                "moderation_results": {
                    "hate": response.hate_result.severity,
                    "self_harm": response.self_harm_result.severity,
                    "sexual": response.sexual_result.severity,
                    "violence": response.violence_result.severity,
                },
            }
        )
    return moderated_segments
