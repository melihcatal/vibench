from typing import Iterable, List

from openai import OpenAI
from speech_models import TranscriptEvent


class CaptionEmbedder:
    def __init__(self, api_key: str | None = None) -> None:
        self.client = OpenAI(api_key=api_key)

    def embed(self, events: Iterable[TranscriptEvent]) -> List[List[float]]:
        texts = [event.text for event in events if event.text]
        if not texts:
            return []
        response = self.client.embeddings.create(model="text-embedding-3-small", input=texts)
        return [item.embedding for item in response.data]
