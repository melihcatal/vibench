import asyncio
import json

from google.cloud import speech_v1p1beta1 as speech
from speech_models import extract_alternatives
from speech_client import get_google_client

# Simple summarizer using OpenAI's ChatGPT (or any summarizer model)
from openai import OpenAI

MODEL_ID = "gpt-4o-mini"  # Example OpenAI model for summarization

async def microphone_generator():
    # Placeholder for microphone stream (see stream_microphone.py)
    raise NotImplementedError

async def summarize_stream(client, config, model_id):
    """Stream audio, collect final transcript, then summarize.", model_id
    responses = client.streaming_recognize(config, microphone_generator())
    transcript_chunks = []
    async for resp in responses:
        for alt in extract_alternatives(resp):
            if alt["is_final"]:
                transcript_chunks.append(alt["transcript"])
    full_transcript = " ".join(transcript_chunks)
    client = OpenAI()
    response = client.chat.completions.create(
        model=model_id,
        messages=[{"role": "user", "content": f"Summarize the following meeting transcript:\n\n{full_transcript}"}],
    )
    summary = response.choices[0].message.content.strip()
    print(f"[SUMMARY] {summary}")

if __name__ == "__main__":
    client = get_google_client()
    config = speech.StreamingRecognitionConfig(
        config=speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
            enable_automatic_punctuation=True,
        ),
        interim_results=True,
    )
    asyncio.run(summarize_stream(client, config, MODEL_ID))