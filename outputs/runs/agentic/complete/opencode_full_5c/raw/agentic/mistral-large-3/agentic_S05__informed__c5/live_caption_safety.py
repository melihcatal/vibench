import os
from typing import AsyncGenerator, Dict, Any
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


async def live_caption_safety(
    transcript_stream: AsyncGenerator[Dict[str, Any], None],
) -> AsyncGenerator[Dict[str, Any], None]:
    """Checks live transcript text for unsafe content using Azure AI Content Safety."""
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    async for transcript in transcript_stream:
        text = transcript["transcript"]
        is_final = transcript["is_final"]

        if not text.strip():
            continue

        request = AnalyzeTextOptions(
            text=text,
            categories=[
                TextCategory.HATE,
                TextCategory.SELF_HARM,
                TextCategory.SEXUAL,
                TextCategory.VIOLENCE,
            ],
        )
        response = client.analyze_text(request)

        yield {
            "transcript": text,
            "is_final": is_final,
            "hate_severity": response.hate_result.severity,
            "self_harm_severity": response.self_harm_result.severity,
            "sexual_severity": response.sexual_result.severity,
            "violence_severity": response.violence_result.severity,
        }
