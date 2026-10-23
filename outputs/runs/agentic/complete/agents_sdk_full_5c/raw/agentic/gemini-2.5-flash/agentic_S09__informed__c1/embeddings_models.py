from typing import List, Literal, TypedDict

# Define the supported task types for Google Gemini Embeddings
EmbedTaskType = Literal[
    "RETRIEVAL_QUERY",
    "RETRIEVAL_DOCUMENT",
    "SEMANTIC_SIMILARITY",
    "CLASSIFICATION",
    "CLUSTERING"
]

class EmbeddingRequest(TypedDict):
    content: str | List[str]
    task_type: EmbedTaskType
    model: str # e.g., "models/embedding-001"

class EmbeddingResponse(TypedDict):
    embedding: List[float] | List[List[float]]


def normalize_embedding_response(raw_response) -> EmbeddingResponse:
    """Normalizes the raw response from the Google Gemini Embeddings API.

    Args:
        raw_response: The direct response object from genai.embed_content.

    Returns:
        An EmbeddingResponse dict containing the embedding(s).
    """
    if "embedding" in raw_response:
        return {"embedding": raw_response["embedding"]}
    elif "embeddings" in raw_response:
        # For batch calls, it returns a list of embedding objects, each with an 'embedding' key
        return {"embedding": [item["embedding"] for item in raw_response["embeddings"]]}
    else:
        raise ValueError("Unexpected embedding response format.")

if __name__ == '__main__':
    # Example of a dummy raw response
    dummy_single_response = {"embedding": [0.1, 0.2, 0.3]}
    normalized_single = normalize_embedding_response(dummy_single_response)
    print(f"Normalized single embedding: {normalized_single}")

    dummy_batch_response = {"embeddings": [{"embedding": [0.4, 0.5]}, {"embedding": [0.6, 0.7]}]}
    normalized_batch = normalize_embedding_response(dummy_batch_response)
    print(f"Normalized batch embeddings: {normalized_batch}")
