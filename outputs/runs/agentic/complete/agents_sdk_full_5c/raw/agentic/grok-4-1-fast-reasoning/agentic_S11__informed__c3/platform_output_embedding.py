import os
import cohere

def get_platform_output_embedding(texts: list[str], model_id: str = "embed-english-v3.0") -> list[list[float]]:
    """
    Embed using Cohere Embed API.
    """
    api_key = os.getenv("COHERE_API_KEY")
    client = cohere.Client(api_key)
    response = client.embed(
        texts=texts,
        model=model_id,
        input_type="search_document"
    )
    return response.embeddings