import os
import json
from observability_models import LogEvent, LogResponse
from observability_client import ManagedLogClient

# Provider-specific credentials (demo uses DeepL for translation)
DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")
GOOGLE_KEY = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
AZURE_TRANSLATOR_KEY = os.getenv("AZURE_TRANSLATOR_KEY")
AMAZON_KEY = os.getenv("AWS_ACCESS_KEY_ID")
ALIBABA_KEY = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")

# Choose provider based on presence of keys (priority order)
if DEEPL_AUTH_KEY:
    CURRENT_PROVIDER = "deepl"
elif GOOGLE_KEY:
    CURRENT_PROVIDER = "google-translate"
elif AZURE_TRANSLATOR_KEY:
    CURRENT_PROVIDER = "azure"
elif AMAZON_KEY:
    CURRENT_PROVIDER = "aws"
elif ALIBABA_KEY:
    CURRENT_PROVIDER = "alibaba"
else:
    raise RuntimeError("No translation provider credentials found")

# Simple helper to call the selected provider
if CURRENT_PROVIDER == "deepl":
    from deepl import DeepL

    deepl_client = DeepL(auth_key=DEEPL_AUTH_KEY)

    def translate_text(text: str, target_lang: str = "FR") -> str:
        result = deepl_client.translate_text(text, target_lang=target_lang)
        return result.translated_text
elif CURRENT_PROVIDER == "google-translate":
    from google.cloud import translate_v2 as translate

    client = translate.Client()

    def translate_text(text: str, target_lang: str = "fr") -> str:
        result = client.translate(text, target_language=target_lang)
        return result["translatedText"]
elif CURRENT_PROVIDER == "azure":
    from azure.ai.translation import TranslationClient

    client = TranslationClient(
        endpoint=os.getenv("AZURE_TRANSLATOR_ENDPOINT"),
        credential=os.getenv("AZURE_TRANSLATOR_KEY"),
    )

    def translate_text(text: str, target_lang: str = "fr") -> str:
        response = client.translate(text, to=target_lang)
        return response[0].translations[0].text
elif CURRENT_PROVIDER == "aws":
    import boto3

    client = boto3.client("translate", region_name="us-east-1")

    def translate_text(text: str, target_lang: str = "fr") -> str:
        response = client.translate_text(
            Text=text, SourceLanguageCode="en", TargetLanguageCode=target_lang
        )
        return response["TranslatedText"]
elif CURRENT_PROVIDER == "alibaba":
    from alibabacloud_alimt20181011.client import Client as AliClient

    client = AliClient(
        access_key_id=ALIBABA_KEY,
        access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
        endpoint="cn-hangzhou.aliyuncs.com",
    )

    def translate_text(text: str, target_lang: str = "fr") -> str:
        response = client.get_translate(
            {"SourceText": text, "SourceLanguage": "en", "TargetLanguage": target_lang}
        )
        return response.get("TranslatedText", "")
else:
    raise NotImplementedError(f"Unsupported translation provider {CURRENT_PROVIDER}")

# Utility to translate support-visible log messages for another locale
SUPPORTED_LOCALES = ["en", "fr", "es", "de"]


def log_message_translate(message: str, target_locale: str = "fr") -> str:
    """Translate support-visible log messages for another locale.",
    "+Uses selected provider or static mappings when available.",
    """
    # Minimal static mapping for demo
    static_map = {
        "Error opening file": {"fr": "Erreur lors de l'ouverture du fichier"},
        "Failed to connect to database": {
            "fr": "Échec de la connexion à la base de données"
        },
    }
    if target_locale in static_map.get(message, {}):
        return static_map[message][target_locale]
    # Fallback to dynamic translation via selected provider
    return translate_text(message, target_locale)
