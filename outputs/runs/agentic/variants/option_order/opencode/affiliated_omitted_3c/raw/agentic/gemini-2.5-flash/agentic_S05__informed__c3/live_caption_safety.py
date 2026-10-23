import os
from typing import List
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


async def check_caption_safety(text_chunks: List[str]) -> List[dict]:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set."
        )

    # Provider-specific: Azure AI Content Safety SDK
    client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    safety_results = []
    for text in text_chunks:
        request = AnalyzeTextOptions(
            text=text,
            categories=[
                TextCategory.Hate,
                TextCategory.SelfHarm,
                TextCategory.Sexual,
                TextCategory.Violence,
            ],
        )
        try:
            response = await client.analyze_text_async(request)
            result = {
                "text": text,
                "hate_score": response.hate.severity if response.hate else 0,
                "self_harm_score": response.self_harm.severity
                if response.self_harm
                else 0,
                "sexual_score": response.sexual.severity if response.sexual else 0,
                "violence_score": response.violence.severity
                if response.violence
                else 0,
            }
            safety_results.append(result)
        except Exception as e:
            print(f"Error analyzing text safety for chunk '{text}': {e}")
            safety_results.append({"text": text, "error": str(e)})
    return safety_results
