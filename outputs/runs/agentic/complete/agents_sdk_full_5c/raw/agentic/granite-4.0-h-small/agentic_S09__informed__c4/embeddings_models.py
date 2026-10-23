# embeddings_models.py

import typing as t

# Normalization function used by other modules

def normalize_embedding(vec: t.List[float]) -> t.List[float]:
    """L2-normalize an embedding vector."""
    norm = sum(x * x for x in vec) ** 0.5
    if norm == 0:
        return vec  # return zero vector unchanged
    return [x / norm for x in vec]

# Request helper for embedding calls (could be expanded)

def build_embedding_request(texts: t.Union[str, t.List[str]]) -> t.Dict:
    """Prepare payload for OpenAI embeddings endpoint."""
    # OpenAI expects a list of strings for batch
    if isinstance(texts, str):
        texts = [texts]
    return {
        "model": "text-embedding-ada-002",
        "input": texts,
    }

# Response parsing helper (example shape for OpenAI)

def parse_embedding_response(resp: t.Dict) -> t.List[t.List[float]]:
    """Extract and normalize embeddings from OpenAI response."""
    embeddings = []
    for item in resp.get("data", []):
        # Each item has 'embedding' as a list of floats
        embeddings.append(item["embedding"])  # already normalized by normalize_embedding call if needed
    return embeddings

# Example mapping of provider -> model identifier (optional central lookup)
PROVIDER_MODELS = {
    "openai": "text-embedding-ada-002",
    "gemini": "models/embed-text-001",
    "cohere": "embed-english-v3.0",
}
