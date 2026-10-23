from typing import List, Dict, Union

# For Google Gemini Embeddings, the input and output formats are relatively straightforward
# The SDK handles much of the serialization/deserialization.


# Example of a simple request model (can be extended if more parameters are needed)
class EmbeddingRequest:
    def __init__(self, text: Union[str, List[str]]):
        self.text = text


# Example of a simple response model (can be extended to include other metadata)
class EmbeddingResponse:
    def __init__(self, embedding_vector: List[float]):
        self.embedding_vector = embedding_vector


def normalize_embedding_response(response) -> List[float]:
    """Normalizes the embedding response from the Google Generative AI SDK."""
    if response and response.embedding:
        return response.embedding
    return []
