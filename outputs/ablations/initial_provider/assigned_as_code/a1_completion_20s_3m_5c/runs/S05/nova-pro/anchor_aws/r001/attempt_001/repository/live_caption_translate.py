import asyncio

from speech_client import get_translate_client

async def translate_captions(captions, target_language):
    translate_client = get_translate_client()
    translated_captions = []
    for caption in captions:
        result = await translate_client.translate_text(Text=caption, SourceLanguageCode='en', TargetLanguageCode=target_language)
        translated_captions.append(result['TranslatedText'])
    return translated_captions