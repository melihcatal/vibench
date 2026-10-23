# [LATER-STEP] live_caption_translate.py
"""Translate live captions into another language using Google Cloud Translation."""

import asyncio
import google.cloud.translate_v2 as translate
from speech_client import extract_alternatives


async def live_translate(transcript_chunk: str, target_lang: str = "fr"):
    """Append a transcript chunk, translate the full text, and return the translated string."""
    # Keep a global buffer (for simplicity, use a mutable default argument)
    cache = live_translate.cache
    cache += transcript_chunk + " "
    # Initialize translation client lazily
    if not hasattr(live_translate, "client"):
        live_translate.client = translate.Client()
    # Translate the accumulated text
    result = live_translate.client.translate(cache, target_language=target_lang)
    return result["translatedText"]


# Cache of accumulated transcript fragments
live_translate.cache = ""

if __name__ == "__main__":
    # Demo: feed a few chunks and print translations
    chunks = ["Hello", " world", "! This is a test."]
    for c in chunks:
        print(asyncio.run(live_translate(c)))
