from google.cloud import translate_v2 as translate
from model_models import ModelResponse
import os


def translate_platform_output(text: str, target_language: str = "es") -> ModelResponse:
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    translated_text = result["translatedText"]
    # The raw_response here will be the full result dictionary from the translation client
    return ModelResponse(
        text=translated_text,
        raw_response=result,
        metadata={"source_language": result["detectedSourceLanguage"]},
    )
