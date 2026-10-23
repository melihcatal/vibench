import os

from openai import OpenAI

from speech_models import TranscriptEvent, normalize_transcript


def caption_embedding(event: TranscriptEvent) -> list[float]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(
        model="text-embedding-3-small", input=normalize_transcript(event.text)
    )
    return list(response.data[0].embedding)
