from typing import Iterable, List

from openai import OpenAI

from speech_models import TranscriptEvent, normalize_text


def embed_caption_chunks(events: Iterable[TranscriptEvent]) -> List[List[float]]:
    client = OpenAI()
    texts = [
        normalize_text(event.text) for event in events if normalize_text(event.text)
    ]
    if not texts:
        return []
    response = client.embeddings.create(model="text-embedding-3-small", input=texts)
    return [item.embedding for item in response.data]
