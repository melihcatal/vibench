import asyncio
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

async def check_live_caption_safety(text: str) -> bool:
    def _sync_check():
        result = client.moderations.create(input=text)
        return result.results[0].flagged
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _sync_check)