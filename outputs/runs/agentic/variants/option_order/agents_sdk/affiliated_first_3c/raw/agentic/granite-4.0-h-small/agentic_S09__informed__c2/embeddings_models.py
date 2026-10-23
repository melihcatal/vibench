import typing

# Request payload for Direct Embeddings API
RequestData = typing.TypedDict(
    "RequestData",
    {
        "query": str | None,
        "texts": list[str] | None,
    },
)

NormalizedEmbedding = dict[str, list[float]]

def normalize_similarity(vec: list[float]) -> list[float]:
    """Normalize vector to unit length."""
    norm = math.sqrt(sum(x * x for x in vec))
    if norm == 0:
        return vec
    return [x / norm for x in vec]

# Helper to convert raw provider response to a common shape
# def normalize_response(raw: dict) -> NormalizedEmbedding:
#     return {
#         "query_embedding": raw.get("query_embedding", []),
#         "document_embeddings": raw.get("document_embeddings", []),
#     }
