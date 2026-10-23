from __future__ import annotations

from openai import OpenAI

from speech_models import SpeechResult


EMBEDDING_MODEL = "text-embedding-3-large"


def transcript_embedding(result: SpeechResult):
    client = OpenAI()
    text = result.text or "\n".join(segment.text for segment in result.segments)
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    return response.data[0].embedding
