import os
import cohere
from model_models import ModelResponse, EmbeddingResult


def get_embedding(response: ModelResponse) -> EmbeddingResult:
    """
    Generates an embedding for the text using Cohere.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    cohere_response = co.embed(
        texts=[response.text], model="embed-english-light-v2.0", truncate="END"
    )

    embedding = cohere_response.embeddings[0]

    return EmbeddingResult(embedding=embedding)
