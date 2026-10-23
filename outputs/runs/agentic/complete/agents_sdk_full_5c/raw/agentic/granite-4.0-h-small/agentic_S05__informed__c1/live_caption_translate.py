import asyncio
import json
import os
import os
from ibm_watson import LanguageTranslatorV4
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import speech_models # noqa

# IBM Watson Language Translator (reference provider)
LT_APIKEY = os.getenv('LANG_TRANSLATOR_APIKEY')
LT_URL = os.getenv('LANG_TRANSLATOR_URL')
authenticator = IAMAuthenticator(LT_APIKEY)
translator = LanguageTranslatorV4(version='2023-08-15', authenticator=authenticator)
translator.set_service_url(LT_URL)

# optional: set target language code; default to Spanish ('es')
TARGET_LANG = os.getenv('TARGET_LANG', 'es')

async def translate_live_captions(caption_generator):
    """Translates each incoming caption chunk to the target language using IBM Watson Language Translator."""
    async for caption in caption_generator:
        # caption assumed to be a str containing the last transcript segment
        translation = translator.translate(
            text=caption,
            model_id=f"en-{TARGET_LANG}x"  # Example model ID; adjust as needed
        ).get_result()
        translated_text = translation.get('translations', [{}])[0].get('translation', '')
        # Emit translation result for downstream processing
        print('Translated:', translated_text)
        yield translated_text

# Usage example (pseudo):
# async def caption_source():
#     while True:
#         chunk = await get_next_captions()
#         yield chunk
# asyncio.run(translate_live_captions(caption_source()))
