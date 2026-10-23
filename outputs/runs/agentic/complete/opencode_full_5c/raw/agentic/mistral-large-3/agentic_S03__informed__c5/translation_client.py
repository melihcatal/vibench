import os
from typing import Optional
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from translation_models import TranslationRequest, TranslationResponse


class AzureTranslationClient:
    """
    Client helper for Azure AI Translator.
    """

    def __init__(self):
        self.key = os.getenv("AZURE_TRANSLATOR_KEY")
        self.region = os.getenv("AZURE_TRANSLATOR_REGION")
        if not self.key or not self.region:
            raise ValueError(
                "AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_REGION must be set."
            )
        self.client = TextTranslationClient(
            credential=TranslatorCredential(self.key, self.region)
        )

    def translate(self, request: TranslationRequest) -> TranslationResponse:
        """
        Translates texts using Azure AI Translator.
        """
        response = self.client.translate(
            content=request.texts,
            to=request.target_languages,
            from_parameter=request.source_language,
            category=request.category,
        )
        translations = {
            target: [item.text for item in response]
            for target in request.target_languages
        }
        return TranslationResponse(translations=translations)


def get_translation_client() -> AzureTranslationClient:
    """
    Returns a configured Azure AI Translator client.
    """
    return AzureTranslationClient()
