import asyncio
from typing import AsyncIterable

import google.cloud.translate_v2 as translate

# Google Cloud Translation API credentials (environment variable)
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
TRANSLATOR = translate.Client()  # automatically reads the JSON key file
TARGET_LANGUAGE = "es"  # example target language; can be set via env var


async def translate_live_captions(captions: AsyncIterable[str]) -> AsyncIterable[str]:
    """Translates each incoming caption chunk into the target language using Google Translate."""
    for chunk in captions:
        # The translate client works synchronously but is fast enough for streaming
        result = TRANSLATOR.translate(chunk, target_language=TARGET_LANGUAGE)
        yield result["translatedText"]


# Example usage with a captions generator (could be from stream_microphone.py)
# async for translated in translate_live_captions(stream_microphone_events):
#     print("Translated: ", translated)
