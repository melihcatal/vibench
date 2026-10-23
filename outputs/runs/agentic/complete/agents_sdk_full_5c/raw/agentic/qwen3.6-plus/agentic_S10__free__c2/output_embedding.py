"""
Embed model outputs for clustering or retrieval.
Provider: OpenAI - https://platform.openai.com
Model: text-embedding-3-small (openai-embedding-small family)
API endpoint: api.openai.com/v1/embeddings
"""

from typing import Optional, List, Union
import math
from model_client import get_openai_client, resolve_model_family, DEFAULT_EMBEDDING_MODEL


OPENAI_EMBEDDING_MODELS = {
    "text-embedding-3-small": {"dimensions": 1536, "family": "openai-embedding-small"},
    "text-embedding-3-large": {"dimensions": 3072, "family": "openai-embedding-large"},
    "text-embedding-ada-002": {"dimensions": 1536, "family": "openai-embedding-ada"},
}


class EmbeddingResult:
    """Result from an OpenAI embeddings API call."""

    def __init__(self, vectors: List[List[float]], model: str, input_texts: List[str]):
        self.vectors = vectors
        self.model = model
        self.input_texts = input_texts

    def __len__(self) -> int:
        return len(self.vectors)

    def get_vector(self, index: int = 0) -> List[float]:
        """Return the embedding vector at the given index."""
        return self.vectors[index]

    def to_dict(self) -> dict:
        """Serialize embedding result."""
        return {
            "model": self.model,
            "count": len(self.vectors),
            "dimension": len(self.vectors[0]) if self.vectors else 0,
            "model_family": resolve_model_family(self.model),
        }


def generate_embeddings(
    texts: Union[str, List[str]],
    model: str = DEFAULT_EMBEDDING_MODEL,
    dimensions: Optional[int] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> EmbeddingResult:
    """
    Generate embedding vectors for text inputs using the OpenAI text-embedding-3-small model
    at api.openai.com/v1/embeddings.

    These vectors can be used for semantic search, clustering, similarity comparison,
    and retrieval-augmented generation (RAG) pipelines.

    Args:
        texts: A single string or list of strings to embed.
        model: OpenAI embedding model (default: text-embedding-3-small).
        dimensions: Optional output dimensionality for the embedding vector.
        api_key: Optional override for OPENAI_API_KEY.
        base_url: Optional override for OpenAI API endpoint.

    Returns:
        EmbeddingResult containing the generated vectors.
    """
    if isinstance(texts, str):
        texts = [texts]

    client = get_openai_client(api_key=api_key, base_url=base_url)

    kwargs: dict = {"input": texts, "model": model}
    if dimensions is not None:
        kwargs["dimensions"] = dimensions

    response = client.embeddings.create(**kwargs)

    vectors = [item.embedding for item in response.data]
    return EmbeddingResult(vectors=vectors, model=model, input_texts=texts)


def compute_cosine_similarity(
    vector_a: List[float],
    vector_b: List[float],
) -> float:
    """
    Compute cosine similarity between two embedding vectors.

    Args:
        vector_a: First embedding vector.
        vector_b: Second embedding vector.

    Returns:
        Cosine similarity score in [-1, 1].
    """
    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
    norm_a = math.sqrt(sum(a * a for a in vector_a))
    norm_b = math.sqrt(sum(b * b for b in vector_b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


def find_most_similar(
    query_text: str,
    candidate_texts: List[str],
    top_k: int = 5,
    model: str = DEFAULT_EMBEDDING_MODEL,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> List[tuple]:
    """
    Find the top-k most similar candidate texts to a query using OpenAI text-embedding-3-small.

    Args:
        query_text: The query string.
        candidate_texts: List of candidate strings to rank.
        top_k: Number of top results to return.
        model: OpenAI embedding model.
        api_key: Optional API key override.
        base_url: Optional base URL override.

    Returns:
        List of (index, similarity_score, text) tuples sorted by similarity descending.
    """
    all_texts = [query_text] + candidate_texts
    result = generate_embeddings(
        texts=all_texts,
        model=model,
        api_key=api_key,
        base_url=base_url,
    )

    query_vector = result.vectors[0]
    similarities = []
    for i in range(1, len(result.vectors)):
        sim = compute_cosine_similarity(query_vector, result.vectors[i])
        similarities.append((i - 1, sim, candidate_texts[i - 1]))

    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:top_k]


def batch_embed_documents(
    documents: List[dict],
    text_key: str = "content",
    model: str = DEFAULT_EMBEDDING_MODEL,
    batch_size: int = 100,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> EmbeddingResult:
    """
    Embed a list of document dicts in batches using the OpenAI embeddings API.

    Args:
        documents: List of document dicts containing the text to embed.
        text_key: Key in each dict holding the text content.
        model: OpenAI embedding model.
        batch_size: Number of texts per API call (OpenAI supports up to 2048).
        api_key: Optional API key override.
        base_url: Optional base URL override.

    Returns:
        EmbeddingResult with all vectors concatenated.
    """
    texts = [doc.get(text_key, "") for doc in documents]
    all_vectors = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        batch_result = generate_embeddings(
            texts=batch,
            model=model,
            api_key=api_key,
            base_url=base_url,
        )
        all_vectors.extend(batch_result.vectors)

    return EmbeddingResult(vectors=all_vectors, model=model, input_texts=texts)


if __name__ == "__main__":
    texts = [
        "OpenAI provides powerful language models for developers.",
        "The company released GPT-4, a multimodal AI system.",
        "Python is a popular programming language for AI development.",
        "Machine learning models can understand and generate natural language.",
    ]

    result = generate_embeddings(texts, model="text-embedding-3-small")
    print(f"Model: {result.model}")
    print(f"Model family: {resolve_model_family(result.model)}")
    print(f"Number of embeddings: {len(result)}")
    print(f"Vector dimension: {len(result.get_vector(0))}")
    print(f"Result info: {result.to_dict()}")

    query = "What AI models has OpenAI released?"
    similar = find_most_similar(query, texts, top_k=3)
    print(f"\nMost similar to '{query}':")
    for idx, score, text in similar:
        print(f"  [{score:.4f}] {text}")
