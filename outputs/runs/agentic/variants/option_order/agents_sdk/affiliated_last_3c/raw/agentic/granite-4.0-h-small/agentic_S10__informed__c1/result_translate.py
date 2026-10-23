import os
from model_client import normalize_response
from model_models import RequestShape

# Using Amazon Translate as the translation service
import boto3

# Environment variables for AWS credentials (already required by DashScope client)
# No additional keys needed if default credentials are available.
translate_client = boto3.client('translate')


def translate_text(text: str, target_language: str = "es") -> str:
    """Translate model output to a target language using Amazon Translate.

    Args:
        text (str): The source text.
        target_language (str): ISO language code (e.g., 'es' for Spanish).

    Returns:
        str: Translated text.
    """
    response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode='auto',
        TargetLanguageCode=target_language
    )
    return response.get('TranslatedText', '')


def translate_response(response: RequestShape, target_language: str = "es") -> RequestShape:
    """Wrap translation over the LLM response content.

    Modifies the response dict in‑place, replacing the generated text with its translation.
    
    Args:
        response (RequestShape): Normalized LLM response.
        target_language (str): Target language code.
    
    Returns:
        RequestShape: Same dict with translated content.
    """
    if response.get("choices"):
        content = response["choices"][0]["message"].get("content", "")
        translated = translate_text(content, target_language)
        response["choices"][0]["message"]["content"] = translated
    return response
