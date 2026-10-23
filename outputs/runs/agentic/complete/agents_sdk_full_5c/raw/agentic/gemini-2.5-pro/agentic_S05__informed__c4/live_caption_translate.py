import os
from typing import List
from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential

def translate_caption_chunk(text: str, target_language: str = "fr") -> str:
    """
    Translates a caption chunk to the target language using Azure AI Translator.

    Args:
        text: The text to translate.
        target_language: The ISO 639-1 code for the target language (e.g., "fr" for French).

    Returns:
        The translated text.
    """
    try:
        key = os.environ["AZURE_TRANSLATOR_KEY"]
        region = os.environ["AZURE_TRANSLATOR_REGION"]
        endpoint = os.environ.get("AZURE_TRANSLATOR_ENDPOINT", f"https://api.cognitive.microsofttranslator.com/")
        
        credential = TranslatorCredential(key, region)
        text_translator_client = TextTranslationClient(endpoint=endpoint, credential=credential)

        response = text_translator_client.translate(content=[text], to_language=[target_language])
        
        translation = response[0].translations[0]
        return translation.text

    except KeyError as e:
        print(f"Error: Environment variable {e} not set.")
        return ""
    except Exception as e:
        print(f"An error occurred during translation: {e}")
        return ""

if __name__ == '__main__':
    # Ensure AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_REGION are set
    if "AZURE_TRANSLATOR_KEY" in os.environ and "AZURE_TRANSLATOR_REGION" in os.environ:
        original_text = "Hello, this is a live caption that needs to be translated."
        translated_text = translate_caption_chunk(original_text, "es")
        print(f"Original: {original_text}")
        print(f"Translated (es): {translated_text}")
    else:
        print("Please set AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_REGION environment variables.")
