import os
import cohere
from model_models import EmbeddingResult

def get_cohere_embeddings(texts: list[str], model: str = "embed-english-v3.0", input_type: str = "classification") -> EmbeddingResult:
    api_key = os.getenv("COHERE_API_KEY")

    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable must be set.")

    co = cohere.Client(api_key)
    response = co.embed(texts=texts, model=model, input_type=input_type)

    return EmbeddingResult(embeddings=response.embeddings, raw_response=response.dict())
