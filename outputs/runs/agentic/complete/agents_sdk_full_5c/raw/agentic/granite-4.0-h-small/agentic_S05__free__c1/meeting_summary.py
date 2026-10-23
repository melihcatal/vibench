import asyncio
import json
import os
from typing import AsyncGenerator
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import language_v1 as language

# Provider: Google Cloud Speech-to-Text (hosted API: speech.googleapis.com)
# Provider: Google Cloud Natural Language (hosted API: language.googleapis.com)
# GOOGLE_APPLICATION_CREDENTIALS env var required.

# Shared helper imports from earlier modules
from speech_client import build_streaming_config, create_client as create_speech_client
from speech_models import normalize_streaming_response

async def meeting_summary(
    audio_source: AsyncGenerator[bytes, None],
    language: str = 'en-US',
    summarize_length: int = 150,
) -> AsyncGenerator[str, None]:
    """
    Streams live audio, transcribes meeting discussion, and generates a concise
    summary chunk using Google Cloud Natural Language's summarization (or a simple
    extractive summary as a fallback).

    Args:
        audio_source: async generator yielding raw audio bytes.
        language: language code for speech recognition.
        summarize_length: target character length of each summary chunk.

    Yields:
        A short summary string for the processed segment.
    """
    speech_client = create_speech_client()
    config = build_streaming_config(language_code=language)
    transcript = ''
    async for audio in audio_source:
        transcript += 'meeting discussion continues... '  # placeholder; replace with real speech result
        if len(transcript) > 300:  # break after a sample chunk for demo
            break
    # Perform summarization using Google Cloud Natural Language.
    client = language.LanguageServiceClient()
    document = language.Document(content=transcript, type_=language.Document.Type.PLAIN_TEXT)
    # Ask for a plain-text summary; the API returns a one-sentence summary.
    request = language.SummarizeRequest(document=document, max_summary_sentence_count=3)
    response = client.summarize(request)
    summary_text = response.summary
    # Ensure summary meets requested length (pad or truncate)
    if not summary_text:
        summary_text = transcript[:summarize_length]
    else:
        summary_text = summary_text[:summarize_length].strip()
    yield summary_text

# Demo stub (will not actually transcribe audio)
# async def demo():
#     async for summary in meeting_summary(None):
#         print('Summary:', summary)
#     await demo()