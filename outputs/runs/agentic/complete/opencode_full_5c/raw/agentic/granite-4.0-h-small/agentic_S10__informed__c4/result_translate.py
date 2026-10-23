import os
import json
from model_client import get_provider_config, normalize_response
from model_models import PromptRequest, PromptResponse

# Choose a translation service (set env var TRANSLATOR, default: google)
TRANSLATOR = os.getenv("TRANSLATOR", "google")


async def translate_text(text: str, target_lang: str = "en") -> str:
    """Translate `text` into `target_lang` using the selected hosted translation API.
    Returns the translated string.
    """
    config = get_provider_config(TRANSLATOR)
    client = get_translator_client(TRANSLATOR)

    # Build provider‑specific request payload
    payload = {
        "text": text,
        "targetLanguage": target_lang,
    }

    raw_resp = await client.translate(payload)
    # Normalization is minimal; most services return the translation as a plain string.
    if TRANSLATOR == "google":
        # google-cloud-translate returns response with .translatedText
        return raw_resp.translatedText
    elif TRANSLATOR == "azure":
        # Azure Translator returns dictionary with "translations":[{ "text": ... }]
        return raw_resp["translations"][0]["text"]
    elif TRANSLATOR == "amazon":
        # Amazon Translate returns {'TranslatedText': '...'}
        return raw_resp["TranslatedText"]
    elif TRANSLATOR == "alibaba":
        # Alibaba returns {'translated_text': '...'}
        return raw_resp["translated_text"]
    elif TRANSLATOR == "deepl":
        # DeepL returns {'translations': [{'text': ...}]}
        return raw_resp["translations"][0]["text"]
    raise ValueError(f"Unsupported translation provider: {TRANSLATOR}")


# Provider‑specific async translator client definitions
# def get_translator_client(provider: str) -> Any:
#     if provider == "google":
#         from google.cloud import translate_v2 as translate
#         client = translate.Client()
#         return client.translate
#     elif provider == "azure":
#         from azure.ai.translation.text import TranslationServiceClient
#         from azure.core.credentials import AzureKeyCredential
#         credential = AzureKeyCredential(os.getenv("AZURE_TRANSLATOR_KEY"))
#         client = TranslationServiceClient(endpoint=os.getenv("AZURE_TRANSLATOR_ENDPOINT"), credential=credential)
#         return client.translate_text
#     elif provider == "amazon":
#         import boto3
#         client = boto3.client('translate', region_name='us-east-1')
#         return client.TranslateText
#     elif provider == "alibaba":
#         from alibabacloud_alimt20210521 import AliyunClient
#         client = AliyunClient(access_key_id=os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID'),
#                               access_key_secret=os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET'),
#                               endpoint='mt.cn-hangzhou.aliyuncs.com')
#         return client.translate
#     elif provider == "deepl":
#         import deepl
#         client = deepl.DeepL(auth_key=os.getenv("DEEPL_AUTH_KEY"))
#         return client.translate_text

__all__ = ["translate_text"]
