import os
import cohere
from speech_models import TranscriptEvent

cohere_client = cohere.Client(os.getenv("COHERE_API_KEY"))

def embed_caption(event: TranscriptEvent) -> list[float]:
    if not event.is_final:
        return []
    response = cohere_client.embed(texts=[event.text], model="embed-english-v3.0")
    return response.embeddings[0]