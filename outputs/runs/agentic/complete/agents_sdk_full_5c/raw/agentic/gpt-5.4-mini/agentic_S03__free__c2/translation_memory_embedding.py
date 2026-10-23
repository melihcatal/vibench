from typing import List

from openai import OpenAI

from translation_client import load_config

OPENAI_EMBEDDING_MODEL = "text-embedding-3-large"


def embed_translated_segments(segments: List[str]) -> List[List[float]]:
    cfg = load_config()
    client = OpenAI(api_key=cfg.api_key) if cfg.api_key else OpenAI()
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=segments)
    return [item.embedding for item in response.data]
