from typing import Dict

from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential


AZURE_TRANSLATOR_KEY = ""
AZURE_TRANSLATOR_REGION = ""


def translate_consent_copy(text: str, target_language: str) -> Dict[str, str]:
    client = TextTranslationClient(
        endpoint="https://api.cognitive.microsofttranslator.com",
        credential=AzureKeyCredential(AZURE_TRANSLATOR_KEY),
        region=AZURE_TRANSLATOR_REGION,
    )
    result = client.translate(content=[text], to=[target_language])
    translation = (
        result[0].translations[0].text if result and result[0].translations else ""
    )
    return {
        "source": text,
        "target_language": target_language,
        "translation": translation,
    }
