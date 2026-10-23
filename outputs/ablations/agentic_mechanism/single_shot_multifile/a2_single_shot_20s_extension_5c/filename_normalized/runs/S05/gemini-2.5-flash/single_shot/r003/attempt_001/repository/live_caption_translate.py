import asyncio
import os
from typing import AsyncIterator

from google.cloud import translate_v3 as translate
from google.api_core.exceptions import GoogleAPIError

from speech_models import TranscriptResult, TranslatedCaption

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")

async def translate_live_captions(
    caption_stream: AsyncIterator[TranscriptResult],
    target_language_code: str = "es"
) -> AsyncIterator[TranslatedCaption]:
    if not PROJECT_ID or PROJECT_ID == "your-gcp-project-id":
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set or is default. Please set it.")

    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{PROJECT_ID}/locations/{location}"

    async for transcript_result in caption_stream:
        if transcript_result.is_final and transcript_result.transcript.strip():
            try:
                response = client.translate_text(
                    request={
                        "parent": parent,
                        "contents": [transcript_result.transcript],
                        "target_language_code": target_language_code,
                        "source_language_code": transcript_result.language_code or "en-US",
                        "mime_type": "text/plain",
                    }
                )
                
                for translation in response.translations:
                    yield TranslatedCaption(
                        original_text=transcript_result.transcript,
                        translated_text=translation.translated_text,
                        source_language=translation.detected_language_code or (transcript_result.language_code or "en-US"),
                        target_language=target_language_code
                    )
            except GoogleAPIError as e:
                print(f"Translation API error: {e}")
                continue
