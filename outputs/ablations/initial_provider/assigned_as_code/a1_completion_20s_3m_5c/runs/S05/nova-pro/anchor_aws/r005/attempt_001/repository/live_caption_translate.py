import asyncio
import os
from google.cloud import translate

translate_client = translate.TranslateClient()

async def live_caption_translate(text, target_language='es'):
    translation = translate_client.translate(text, target_language=target_language)
    return translation['translatedText']