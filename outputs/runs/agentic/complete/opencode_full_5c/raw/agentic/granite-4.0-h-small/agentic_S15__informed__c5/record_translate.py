import os

# Choose ONE concrete translation service and configure its auth env vars.
# Example: Azure AI Translator (REST SDK)
# from azure.ai.translation import TranslationClient
# translator = TranslationClient(endpoint=os.getenv('AZURE_TRANSLATOR_ENDPOINT'), credential=AzureKeyCredential(os.getenv('AZURE_TRANSLATOR_KEY')))

# Example: Amazon Translate (boto3 SDK)
# import boto3
# translate = boto3.client('translate', region_name='us-east-1')

# Example: Google Cloud Translation (SDK)
# from google.cloud import translate_v2 as translate
# client = translate.Client(credentials=os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))

# For illustration we use DeepL's REST SDK (deepl)
from deepl import DeepL

api_key = os.getenv("DEEPL_AUTH_KEY")
translator = DeepL(auth_key=api_key)


def translate_fields(record: dict, target_lang: str = "es") -> dict:
    """Translate user‑facing string fields of a document to the target language.

    Args:
        record (dict): Document payload containing string values.
        target_lang (str): ISO language code (e.g., 'es' for Spanish).

    Returns:
        dict: New document with translated text fields.
    """
    # Simple approach: translate every top‑level string value
    translated = {}
    for key, value in record.items():
        if isinstance(value, str):
            # provider‑specific call; here DeepL's translate_text
            result = translator.translate_text(text=value, target_lang=target_lang)
            translated[key] = result["text"]
        else:
            # retain non‑string values unchanged
            translated[key] = value
    return translated
