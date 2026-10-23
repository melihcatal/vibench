from __future__ import annotations

from typing import List

from openai import OpenAI

from speech_client import SpeechServiceConfig, get_client


def transcript_embedding(segments: List[str]) -> List[List[float]]:
    config = SpeechServiceConfig.from_env()
    client: OpenAI = get_client(config)
    response = client.embeddings.create(model=config.embedding_model, input=segments)
    return [item.embedding for item in response.data]
