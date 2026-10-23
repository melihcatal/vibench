import asyncio
import json
import os
import sys
from dataclasses import dataclass
from typing import AsyncIterator, Optional

import httpx


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


@dataclass
class CaptionEvent:
    text: str
    language: str = "en"


class OpenAITranslator:
    def __init__(self, api_key: str, target_language: str) -> None:
        self.api_key = api_key
        self.target_language = target_language

    async def translate(self, text: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": f"Translate live captions into {self.target_language}. Return only the translation."},
                {"role": "user", "content": text},
            ],
            "temperature": 0.2,
        }
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(OPENAI_API_URL, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
        return data["choices"][0]["message"]["content"].strip()


async def read_captions(stream: AsyncIterator[str], translator: OpenAITranslator) -> None:
    async for line in stream:
        line = line.strip()
        if not line:
            continue
        event = CaptionEvent(text=line)
        translated = await translator.translate(event.text)
        print(translated, flush=True)


async def stdin_stream() -> AsyncIterator[str]:
    loop = asyncio.get_running_loop()
    while True:
        line = await loop.run_in_executor(None, sys.stdin.readline)
        if not line:
            break
        yield line


async def main() -> None:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY is required")
    target_language = os.environ.get("TARGET_LANGUAGE", "Spanish")
    translator = OpenAITranslator(api_key=api_key, target_language=target_language)
    await read_captions(stdin_stream(), translator)


if __name__ == "__main__":
    asyncio.run(main())
