from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem
from storage_models import ConfigType, PayloadType
import os

def stored_text_translate(payload: PayloadType, config: ConfigType = None) -> PayloadType:
    config = config or {}
    # Azure Translator endpoint and key from config or environment variables
    endpoint = config.get("azure_translator_endpoint", os.environ.get("AZURE_TRANSLATOR_ENDPOINT"))
    key = config.get("azure_translator_key", os.environ.get("AZURE_TRANSLATOR_KEY"))
    
    source_text = payload["text"]
    target_language = payload.get("target_language", "en") # Default to English

    if not all([endpoint, key, source_text]):
        raise ValueError("Missing required parameters: Azure Translator endpoint, key, source text.")

    # Authenticate and create client
    credential = TranslatorCredential(key, endpoint)
    client = TextTranslationClient(endpoint=endpoint, credential=credential)

    # Perform translation
    try:
        # The `translate` method expects a list of InputTextItem objects
        response = client.translate(target_language=target_language, content=[InputTextItem(text=source_text)])
    except Exception as e:
        return {"error": f"Azure AI Translator failed: {str(e)}"}

    translated_text = []
    if response:
        for translation_result in response:
            if translation_result.translations:
                for translation in translation_result.translations:
                    translated_text.append(translation.text)

    return {"translated_text": "\n".join(translated_text)}
