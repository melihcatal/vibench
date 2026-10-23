import asyncio
import json

from google.cloud import speech_v1p1beta1 as speech
from speech_models import extract_alternatives
from speech_client import get_google_client

# Embedding example using OpenAI's text-embedding-3 model
from openai import OpenAI

EMBED_MODEL = "text-embedding-3-large"  # high-quality embedding


async def microphone_generator():
    # Placeholder for microphone stream (see stream_microphone.py)
    raise NotImplementedError


async def embed_stream(client, config):
    """Stream audio, capture final captions, and compute embeddings."""
    responses = client.streaming_recognize(config, microphone_generator())
    embeddings = []
    async for resp in responses:
        for alt in extract_alternatives(resp):
            if alt["is_final"]:
                text = alt["transcript"]
                client = OpenAI()
                resp = client.embeddings.create(
                    model=EMBED_MODEL,
                    input=text,
                )
                vec = resp.data[0].embedding  # numpy-like array
                embeddings.append({"text": text, "embedding": vec.tolist()})
    print(f"Collected {len(embeddings)} embeddings.")
    return embeddings


if __name__ == "__main__":
    client = get_google_client()
    config = speech.StreamingRecognitionConfig(
        config=speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
            enable_automatic_punctuation=True,
        ),
        interim_results=False,  # we need final transcripts
    )
    asyncio.run(embed_stream(client, config))
