import os
from openai import OpenAI
from translation_models import EmbeddingRequest, EmbeddingResponse

def embed_translated_segment(request: EmbeddingRequest) -> EmbeddingResponse:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.embeddings.create(
        input=[request.text],
        model="text-embedding-ada-002"  # Concrete model identifier
    )

    embedding = response.data[0].embedding
    return EmbeddingResponse(embedding=embedding)
