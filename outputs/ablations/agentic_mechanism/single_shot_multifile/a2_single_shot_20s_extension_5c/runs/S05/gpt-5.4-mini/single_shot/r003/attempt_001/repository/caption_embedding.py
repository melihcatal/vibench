from typing import List

from openai import OpenAI

from speech_client import load_speech_config


def embed_caption_chunks(chunks: List[str]) -> List[List[float]]:
    config = load_speech_config()
    client = OpenAI(api_key=config.api_key or None)
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=chunks,
    )
    return [item.embedding for item in response.data]
