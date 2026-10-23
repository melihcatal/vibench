import asyncio
import aiohttp
import json
from speech_client import SpeechClient
from speech_models import SpeechModels

# Google Cloud Translation (service=Cloud Translation)
# SDK: google-cloud-translate
# Auth: GOOGLE_APPLICATION_CREDENTIALS

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not GOOGLE_APPLICATION_CREDENTIALS:
    raise ValueError("Environment variable GOOGLE_APPLICATION_CREDENTIALS not set")

async def translate_live_captions(source_lang="en", target_lang="es"):
    """
    Streams audio via SpeechClient (e.g., Google Speech-to-Text), translates each chunk,
    and yields translated captions.
    """
    client = SpeechClient("google")
    translator =
        google.cloud.translate_v2.Client(credentials=google.auth.credentials.Credentials.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS))
    async for chunk in client.stream_microphone():
        transcript = client._normalize_response(chunk)  # placeholder for real normalization
        if not transcript:
            continue
        translation = translator.translate(transcript, target_language=target_lang, source_language=source_lang)
        yield translation["translatedText"]

if __name__ == "__main__":
    async def demo():
        async for line in translate_live_captions():
            print(f"Translated: {line}")
            await asyncio.sleep(1)
    asyncio.run(demo())
