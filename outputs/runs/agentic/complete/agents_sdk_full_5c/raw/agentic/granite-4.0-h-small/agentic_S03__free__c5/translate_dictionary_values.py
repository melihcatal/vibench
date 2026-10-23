import os
import json
import httpx
import asyncio
from typing import List, Dict

TRANSLATION_SERVICE_URL = os.getenv('TRANSLATION_SERVICE_URL', 'https://api.example.com/translate')
API_KEY = os.getenv('TRANSLATION_API_KEY')

async def translate_dict(d: Dict[str, str], source_lang: str = 'en', target_lang: str = 'es') -> Dict[str, str]:
    results = {}
    async with httpx.AsyncClient() as client:
        for key, text in d.items():
            payload = {"text": text, "source": source_lang, "target": target_lang}
            headers = {"Authorization": f"Bearer {API_KEY}"}
            resp = await client.post(TRANSLATION_SERVICE_URL, json=payload, headers=headers)
            resp.raise_for_status()
            results[key] = resp.json()['translatedText']
    return results

if __name__ == '__main__':
    sample_dict = {'greeting': 'Hello', 'farewell': 'Goodbye'}
    translated = asyncio.run(translate_dict(sample_dict))
    print('Translated dict:', translated)
