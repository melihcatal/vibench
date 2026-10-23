from typing import Iterable, List

from openai import OpenAI

from speech_models import TranscriptChunk, normalize_text


def embed_caption_chunks(chunks: Iterable[TranscriptChunk]) -> List[List[float]]:
    client = OpenAI()
    texts = [normalize_text(chunk.text) for chunk in chunks if chunk.text]
    if not texts:
        return []
    response = client.embeddings.create(model="text-embedding-3-small", input=texts)
    return [item.embedding for item in response.data]
