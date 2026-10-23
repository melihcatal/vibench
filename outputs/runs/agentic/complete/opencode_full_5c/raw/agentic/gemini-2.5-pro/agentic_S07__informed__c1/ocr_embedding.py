import os
from openai import OpenAI
from document_models import EmbeddingVector


def get_text_embedding(text: str) -> EmbeddingVector:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY must be set in environment variables.")

    client = OpenAI(api_key=api_key)

    model = "text-embedding-3-small"

    response = client.embeddings.create(input=text, model=model)

    return EmbeddingVector(embedding=response.data[0].embedding, model=model)
