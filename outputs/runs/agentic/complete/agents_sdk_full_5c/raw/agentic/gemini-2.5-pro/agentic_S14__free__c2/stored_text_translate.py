import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.text import TextTranslationClient
from storage_models import TranslationResult

def translate_text_content(text: str, source_language: str, target_languages: list[str]) -> list[TranslationResult]:
    """
    Translates text using Azure AI Translator service.

    :param text: The text to translate.
    :param source_language: The source language code (e.g., 'en').
    :param target_languages: A list of target language codes (e.g., ['fr', 'es']).
    :return: A list of TranslationResult objects.
    """
    try:
        endpoint = os.environ["AZURE_TRANSLATOR_ENDPOINT"]
        subscription_key = os.environ["AZURE_TRANSLATOR_KEY"]
        region = os.environ["AZURE_TRANSLATOR_REGION"]
    except KeyError:
        raise EnvironmentError("Azure Translator environment variables not set.")

    credential = AzureKeyCredential(subscription_key)
    
    text_translator_client = TextTranslationClient(
        endpoint=endpoint,
        credential=credential,
        region=region
    )
    
    response = text_translator_client.translate(
        content=[text],
        to=target_languages,
        from_lang=source_language
    )
    
    results = []
    translation_response = response[0] if response else None
    
    if translation_response and translation_response.translations:
        for translation in translation_response.translations:
            results.append(
                TranslationResult(
                    original_text=text,
                    translated_text=translation.text,
                    source_language=translation_response.detected_language.language,
                    target_language=translation.to
                )
            )

    return results
