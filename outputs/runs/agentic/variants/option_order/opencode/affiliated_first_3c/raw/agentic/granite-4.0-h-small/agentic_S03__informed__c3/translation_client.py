import os
import json

# Provider configuration examples – set the appropriate environment variable for your chosen service
DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
AZURE_TRANSLATOR_KEY = os.getenv("AZURE_TRANSLATOR_KEY")
AZURE_TRANSLATOR_REGION = os.getenv("AZURE_TRANSLATOR_REGION")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")


def get_translation_service_client(provider: str):
    """Return a configured client for the requested provider.

    Supported providers (case‑insensitive):
        'deepl', 'google', 'azure', 'amazon', 'alibaba', 'watsonx'
    """
    provider = provider.lower()
    if provider == "deepl":
        from deepl import DeepL

        return DeepL(auth_key=DEEPL_AUTH_KEY)
    elif provider == "google":
        from google.cloud import translate_v2 as translate

        return translate.Client()
    elif provider == "azure":
        from azure.ai.translation.text import TextTranslationClient
        from azure.core.credentials import AzureKeyCredential

        credential = AzureKeyCredential(AZURE_TRANSLATOR_KEY)
        return TextTranslationClient(
            endpoint=f"https://{AZURE_TRANSLATOR_REGION}.api.cognitive.microsoft.com/",
            credential=credential,
        )
    elif provider == "amazon":
        import boto3

        return boto3.client(
            "translate",
            region_name="us-east-1",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
    elif provider == "alibaba":
        from alibabacloud_alimt20200331.client import Client as AliMtClient

        return AliMtClient(
            endpoint="mt-cn-hangzhou.aliyuncs.com",
            access_key_id=ALIBABA_CLOUD_ACCESS_KEY_ID,
            access_key_secret=ALIBABA_CLOUD_ACCESS_KEY_SECRET,
        )
    elif provider == "watsonx":
        from ibm_watson import LanguageTranslatorV3
        from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

        authenticator = IAMAuthenticator(WATSONX_API_KEY)
        return LanguageTranslatorV3(
            version="2023-11-01",
            service_url=f"https://{WATSONX_PROJECT_ID}.api.watson.com/",
            authenticator=authenticator,
        )
    else:
        raise ValueError(f"Unsupported provider: {provider}")


def normalize_request(payload, provider):
    """Translate a raw payload into the shape expected by the target provider.

    Returns a dict ready for the provider's SDK/REST call.
    """
    provider = provider.lower()
    if provider in ("deepl", "google", "amazon", "watsonx"):
        return {
            "text": payload.get("text"),
            "source_lang": payload.get("source"),
            "target_lang": payload.get("target"),
        }
    elif provider == "azure":
        return {
            "source_text": {"text": payload["text"]},
            "target_language": payload["target"],
        }
    elif provider == "alibaba":
        return {
            "SourceLanguage": payload["source"],
            "TargetLanguage": payload["target"],
            "Text": payload["text"],
        }
    raise ValueError(f"Unsupported provider for normalization: {provider}")


def normalize_response(response, provider):
    """Normalize provider‑specific responses into a common dict: {"translated_text": ", "source_lang": , "target_lang": }."""
    provider = provider.lower()
    if provider in ("deepl", "google", "amazon", "watsonx"):
        resp = response
        return {
            "translated_text": resp.get("translatedText"),
            "source_lang": resp.get("detectedSourceLanguage"),
            "target_lang": resp.get("target_lang"),
        }
    elif provider == "azure":
        return {
            "translated_text": response["translation"][0]["text"],
            "source_lang": "unknown",
            "target_lang": response["translation"][0]["to"],
        }
    elif provider == "alibaba":
        return {
            "translated_text": response["TranslatedText"],
            "source_lang": response["SourceLanguage"],
            "target_lang": response["TargetLanguage"],
        }
    raise ValueError(f"Unsupported provider for normalization: {provider}")
