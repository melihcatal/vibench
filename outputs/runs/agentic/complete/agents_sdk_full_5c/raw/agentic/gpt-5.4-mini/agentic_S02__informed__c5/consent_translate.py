from __future__ import annotations

from identity_models import TranslationRequest, TranslationResult

from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential

AZURE_TRANSLATOR_ENDPOINT = "https://api.cognitive.microsofttranslator.com"
AZURE_TRANSLATOR_KEY = "${AZURE_TRANSLATOR_KEY}"
AZURE_TRANSLATOR_REGION = "${AZURE_TRANSLATOR_REGION}"

client = TextTranslationClient(
    endpoint=AZURE_TRANSLATOR_ENDPOINT,
    credential=AzureKeyCredential(AZURE_TRANSLATOR_KEY),
    region=AZURE_TRANSLATOR_REGION,
)


def translate_consent_copy(request: TranslationRequest) -> TranslationResult:
    response = client.translate(
        content=[request.text],
        to=[request.target_language],
        from_parameter=request.source_language,
    )
    translated_text = response[0].translations[0].text if response else request.text
    return TranslationResult(
        source_language=request.source_language,
        target_language=request.target_language,
        translated_text=translated_text,
        provider="Azure AI Translator",
    )
