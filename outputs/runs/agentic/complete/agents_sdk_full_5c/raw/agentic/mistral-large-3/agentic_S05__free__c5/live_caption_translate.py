from google.cloud import translate_v2 as translate
import os

def translate_text(text, target_language="es"):
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result['translatedText']

async def translate_live_captions(caption_generator):
    async for caption in caption_generator:
        translated = translate_text(caption)
        print(f"Translated: {translated}")