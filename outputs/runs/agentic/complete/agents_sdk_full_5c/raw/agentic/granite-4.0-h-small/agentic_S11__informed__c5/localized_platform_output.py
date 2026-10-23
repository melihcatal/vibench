# localized_platform_output.py
# Managed Model Platform Workflow: translate model output to another locale
# Provider: Azure AI Translator
import os
from azure.ai.translation import TranslationClient
from azure.core.credentials import AzureKeyCredential

# Load credentials from environment variables
AZURE_TRANSLATOR_KEY = os.getenv("AZURE_TRANSLATOR_KEY")
AZURE_TRANSLATOR_REGION = os.getenv("AZURE_TRANSLATOR_REGION", "global")

target_locale = os.getenv("TARGET_LOCALE", "es")  # default: Spanish

translator_client = TranslationClient(
    endpoint=f"https://{AZURE_TRANSLATOR_REGION}.translator.azure.com",
    credential=AzureKeyCredential(AZURE_TRANSLATOR_KEY),
)

def translate_text(text: str, target_lang: str = target_locale) -> dict:
    """Translate text using Azure AI Translator and return structured result.

    Returns dict with 'translatedText' and 'sourceLanguage'.
    """
    response = translator_client.translate(text=text, target_language=target_lang)
    translation = response.translations[0]
    return {
        "translatedText": translation.text,
        "detectedSourceLanguage": translation.detected_language.language,
    }

if __name__ == "__main__":
    # Example usage
    source_text = "Hello, how are you today?"
    translation = translate_text(source_text)
    print(translation)
