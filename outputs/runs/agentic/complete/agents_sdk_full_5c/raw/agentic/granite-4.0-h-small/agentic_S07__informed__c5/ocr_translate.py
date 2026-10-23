import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.texttranslation import TextTranslationClient
from document_models import OcrResult

def azure_translate(ocr_result: OcrResult, target_lang: str = "en") -> str:
    """Translate OCR text using Azure AI Translator Service.
    Returns the translated text.
    """
    endpoint = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
    api_key = os.getenv("AZURE_TRANSLATOR_KEY")
    if not endpoint or not api_key:
        raise RuntimeError("Azure Translator credentials not configured")
    client = TextTranslationClient(endpoint=endpoint, credential=AzureKeyCredential(api_key))
    response = client.translate_text([ocr_result.full_text], to_language=target_lang)
    translation = response.translations[0].translations[0].text
    return translation
