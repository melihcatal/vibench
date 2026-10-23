import os
import json
from model_models import ModelResponse

def localized_platform_output(response: ModelResponse, target_locale: str = "es") -> ModelResponse:
    """Translate platform model output to another locale using Google Cloud Translation.

    Args:
        response: Original model response.
        target_locale: BCP-47 language tag for the desired locale (e.g., 'es', 'fr').

    Returns:
        A ModelResponse with translated output and metadata indicating translation.
    """
    from google.cloud import translate_v2 as translate
    client = translate.Client()
    translated = client.translate(response.output, target_language=target_locale)
    return ModelResponse(
        output=translated["translatedText"],
        metadata={
            **response.metadata,
            "translation": {
                "target_locale": target_locale,
                "source": "provider_output",
                "service": "google-cloud-translation",
            },
        },
    )
