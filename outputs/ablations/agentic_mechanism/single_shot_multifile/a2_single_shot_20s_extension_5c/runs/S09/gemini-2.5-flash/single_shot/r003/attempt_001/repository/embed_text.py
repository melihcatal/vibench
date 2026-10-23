import os
from openai import OpenAI
from embeddings_models import EmbeddingResponse

def embed_text(text: str) -> EmbeddingResponse:
    """Generates an embedding vector for a single text string using OpenAI."""
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    model_name = "text-embedding-3-small"
    response = client.embeddings.create(
        input=[text],
        model=model_name
    )
    embedding = response.data[0].embedding
    return EmbeddingResponse(text=text, embedding=embedding, model=model_name)