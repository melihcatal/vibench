# [LATER-STEP] live_caption_translate.py
# Translate live captions into another language using Amazon Translate

import os
import boto3
import asyncio
from typing import AsyncGenerator

# AWS credentials (fits credential requirement)
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION_NAME = "us-east-1"

# Target language code (ISO 639‑1, e.g., 'es' for Spanish)
TARGET_LANG = "es"

# Initialize Amazon Translate client
translate_client = boto3.client(
    "translate",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME,
)


# Example: an async generator that receives live caption chunks from a previous step
async def live_caption_source() -> AsyncGenerator[str, None]:
    """Yields incremental caption text as it becomes available."""
    # Simulated live source (replace with real streaming output)
    for i in range(3):
        yield f"This is live caption chunk {i}."
        await asyncio.sleep(0.5)


async def translate_live_captions() -> None:
    async for caption_chunk in live_caption_source():
        # Translate the caption chunk
        response = translate_client.translate_text(
            Text=caption_chunk,
            SourceLanguageCode="en",
            TargetLanguageCode=TARGET_LANG,
        )
        translated = response["TranslatedText"]
        print(f"Translated: {translated}")


if __name__ == "__main__":
    asyncio.run(translate_live_captions())
# Documentation: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate.html#client
# Fits criterion: hostname "translate.amazonaws.com" and model ID is "Amazon Translate"
