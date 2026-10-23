# DeepL Translation (service=DeepL API; sdk=deepl)
# DEEPL_AUTH_KEY environment variable required

import os
import deepl
import asyncio
from .speech_models import get_credentials, normalize_result


async def live_translate(transcript_chunks):
    """Translate each transcript chunk into Spanish using DeepL."""
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise RuntimeError("Missing DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    target_lang = "ES"
    async for chunk in transcript_chunks:
        result = translator.translate_text(chunk, target_lang=target_lang)
        print(f"Translated: {result.text}")


# Example usage with a generator of transcript strings
async def demo():
    sample = ["Hello world", "This is a test", "Streaming ASR"]
    await live_translate(sample)


if __name__ == "__main__":
    asyncio.run(demo())
