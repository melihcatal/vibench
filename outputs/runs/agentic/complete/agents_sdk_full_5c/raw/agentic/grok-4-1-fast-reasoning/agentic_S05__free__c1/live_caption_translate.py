import asyncio
from google.cloud import translate_v2 as translate

async def translate_live_caption(caption: str, target_language: str = 'es') -> str:
    def _sync_translate():
        client = translate.Client()
        if isinstance(caption, list):
            caption = caption[0]
        result = client.translate(caption, target_language=target_language)
        return result['translatedText']
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _sync_translate)