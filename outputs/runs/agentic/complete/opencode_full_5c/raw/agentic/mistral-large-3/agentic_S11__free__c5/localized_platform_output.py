from typing import Dict, Any
from model_models import ChatResponse
from google.cloud import translate_v2 as translate


def localized_platform_output(
    response: ChatResponse,
    target_language: str = "es",
) -> Dict[str, Any]:
    """
    Translates Azure AI Inference model output using Google Cloud Translation API.
    """
    translate_client = translate.Client()
    result = translate_client.translate(
        response.content,
        target_language=target_language,
    )

    return {
        "translated_text": result["translatedText"],
        "detected_source_language": result["detectedSourceLanguage"],
        "target_language": target_language,
    }
