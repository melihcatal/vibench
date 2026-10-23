from typing import Iterable, List

from openai import OpenAI

from speech_client import load_speech_config


def caption_embedding(chunks: Iterable[str]) -> List[List[float]]:
    config = load_speech_config("openai", model="text-embedding-3-small")
    client = OpenAI(api_key=config.api_key)
    response = client.embeddings.create(model="text-embedding-3-small", input=list(chunks))
    return [item.embedding for item in response.data]
