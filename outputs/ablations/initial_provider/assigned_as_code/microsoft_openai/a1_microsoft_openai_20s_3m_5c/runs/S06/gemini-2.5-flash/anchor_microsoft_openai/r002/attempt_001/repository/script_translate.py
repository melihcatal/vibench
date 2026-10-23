import os
from azure.ai.translator.text import TextTranslationClient, TextTranslationApiVersion
from azure.core.credentials import AzureKeyCredential
from speech_models import TranslationPayload

def script_translate(payload: TranslationPayload):
    endpoint = os.environ.get('AZURE_TRANSLATOR_ENDPOINT')
    key = os.environ.get('AZURE_TRANSLATOR_KEY')
    region = os.environ.get('AZURE_TRANSLATOR_REGION')

    if not endpoint or not key or not region:
        raise ValueError("AZURE_TRANSLATOR_ENDPOINT, AZURE_TRANSLATOR_KEY, and AZURE_TRANSLATOR_REGION environment variables must be set.")

    client = TextTranslationClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
        region=region,
        api_version=TextTranslationApiVersion.V3_0
    )

    response = client.translate(content=[{"text": payload.text}], to=[payload.target_language], from_parameter=payload.source_language)
    
    if response and response[0].translations:
        translated_text = response[0].translations[0].text
        return {"translated_text": translated_text, "source_language": response[0].detected_language.language}
    else:
        raise RuntimeError("Translation failed or no translations found.")
