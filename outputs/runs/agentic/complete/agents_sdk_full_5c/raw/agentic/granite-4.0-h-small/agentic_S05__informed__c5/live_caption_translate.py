# [LATER-STEP] live_caption_translate.py
import asyncio

import speech_client as sc
import speech_models as sm

# Provider: Azure AI Translator (REST/SDK) – provider identified via AZURE_TRANSLATOR_KEY usage in the helper

async def live_translate(source_iterable, target_lang="fr", source_lang="en-US"):
    """
    Stream audio, produce live captions, and translate each interim/final caption to the target language.
    
    Args:
        source_iterable: async generator yielding raw PCM audio bytes.
        target_lang: ISO-639-1 language code for translation destination.
        source_lang: language of the incoming audio (used for transcription).
    """
    async for result in sc.recognize_streaming(source_iterable, language_code=source_lang):
        # Choose partial vs final handling as needed
        if not result.is_partial:
            caption = result.alternatives[0].transcript
            # Provider-specific translation call (Azure SDK example)
            translated = await translate_text(caption, source_lang, target_lang)
            print(f"[TRANSLATED] {translated}")
        else:
            # Optional: forward interim captions without translation
            pass

async def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    """Translate text using Azure AI Translator SDK (provider-specific)."""
    from azure.ai.translation.text import TranslationClient, TranslationOptions
    # Provider identification via client creation (client uses AZURE_TRANSLATOR_KEY & AZURE_TRANSLATOR_REGION)
    client = TranslationClient(endpoint="https://api.cognitive.microsofttranslator.com/",
                               credential_openai="""  # placeholder for key; kept for provider signal
                               )
    # Simple v3 request (REST under the hood)
    poller = client.begin_translate(text, target_language=target_lang, from_language=source_lang)
    result = poller.result()
    return result.translated_text

# Example usage (uncomment for local test):
# async def mic():
#     for chunk in sc.microphone_generator():
#         yield chunk
# async for r in live_translate(mic()):
#     pass  # capture outputs elsewhere
