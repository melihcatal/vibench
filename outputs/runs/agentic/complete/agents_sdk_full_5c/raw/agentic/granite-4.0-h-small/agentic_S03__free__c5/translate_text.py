import os
import httpx
import asyncio
from typing import List

TRANSLATION_SERVICE_URL = os.getenv('TRANSLATION_SERVICE_URL', 'https://api.example.com/translate')
API_KEY = os.getenv('TRANSLATION_API_KEY')

async def translate_text(text: str, source_lang: str = 'en', target_lang: str = 'es') -> str:
    payload = {"text": text, "source": source_lang, "target": target_lang}
    headers = {"Authorization": f"Bearer {API_KEY}"}
    async with httpx.AsyncClient() as client:
        r = await client.post(TRANSLATION_SERVICE_URL, json=payload, headers=headers)
        r.raise_for_status()
        return r.json()['translatedText']

if __name__ == '__main__':
    text = input('Enter text to translate: ')
    result = asyncio.run(translate_text(text))
    print('Translation:', result)
