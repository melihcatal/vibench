import asyncio
import json
from typing import Optional
from deepgram import Deepgram
from speech_client import get_client
from speech_models import normalize_transcript

# ---------------------------
# Translation integration using Amazon Translate (boto3)
# ---------------------------

# Boto3 credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY) must be set in env.
import boto3

# Helper to invoke Amazon Translate
translate_client = boto3.client(
    "translate",
    ServiceName="Amazon Translate",
    region_name="us-east-1",  # adjust region if needed
)


def translate_text(text: str, target_lang: str = "es") -> Optional[str]:
    """Translate using Amazon Translate."""
    try:
        resp = translate_client.translate_text(
            Text=text,
            SourceLanguageCode="en",  # source can be inferred or explicit
            TargetLanguageCode=target_lang,
        )
        return resp.get("TranslatedText")
    except Exception as exc:
        print(json.dumps({"error": str(exc)}))
        return None


async def live_translate_caption():
    # Simulated streaming source (placeholder)
    async def microphone_chunks():
        for i in range(4):
            yield b"speech_chunk_"
            await asyncio.sleep(0.7)

    # Configure streaming to Deepgram with punctuation & language detection
    client = get_client()
    listen_config = {"language": "en-US", "punctuation": True}
    source = client.listen(source=microphone_chunks(), **listen_config)

    async for result in source.listen():
        # Process only final transcripts
        if result.get("is_final"):
            norm = normalize_transcript(result)
            translated = translate_text(norm["transcript"], target_lang="es")
            if translated:
                print(json.dumps({"translated": translated}))


# Run when file executed directly
if __name__ == "__main__":
    asyncio.run(live_translate_caption())
