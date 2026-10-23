import os
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.core.credentials import AzureKeyCredential

from speech_models import TranslatedCaption

def translate_caption(text: str, target_language: str = "fr") -> TranslatedCaption | None:
    """
    Translate live captions into another language using Azure AI Translator.
    """
    try:
        # Get configuration from environment variables
        translator_key = os.environ["AZURE_TRANSLATOR_KEY"]
        translator_region = os.environ["AZURE_TRANSLATOR_REGION"]
        
        # Create a client
        credential = TranslatorCredential(translator_key, translator_region)
        text_translator_client = TextTranslationClient(credential=credential)

        # Make the translation request
        response = text_translator_client.translate(
            content=[{"text": text}],
            to_language=[target_language],
        )

        if response and response[0].translations:
            translation = response[0].translations[0]
            return TranslatedCaption(
                original_text=text,
                translated_text=translation.text,
                target_language=translation.to
            )
        return None

    except KeyError as e:
        print(f"Error: Environment variable {e} not set for Azure Translator.")
        return None
    except Exception as e:
        print(f"An error occurred during translation: {e}")
        return None
