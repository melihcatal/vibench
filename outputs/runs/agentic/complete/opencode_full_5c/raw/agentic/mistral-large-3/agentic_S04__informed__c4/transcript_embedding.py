import os
from openai import OpenAI
from .speech_models import EmbeddingRequest, EmbeddingResponse


def get_transcript_embedding(text: str) -> EmbeddingResponse:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.embeddings.create(input=text, model="text-embedding-ada-002")

    return EmbeddingResponse(embedding=response.data[0].embedding)
