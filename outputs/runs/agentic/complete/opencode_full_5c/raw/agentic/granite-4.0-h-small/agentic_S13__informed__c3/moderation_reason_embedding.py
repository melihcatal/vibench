# moderation_reason_embedding.py
# [LATER-STEP] Embed moderation rationales for case retrieval

# Provider selection – use OpenAI embeddings as an example
PROVIDER = "openai"


# -----------------------------------------------------------------------------
# Public API: generate embeddings for moderation rationales (reasons)
# -----------------------------------------------------------------------------
def embed_reasons(reasons: list) -> list:
    """Produce embeddings for a list of moderation explanation strings.

    Args:
        reasons: List of textual rationales returned by a moderator.

    Returns:
        List of embedding vectors (as lists of floats) ready for vector search.
    """
    if PROVIDER == "openai":
        import openai

        openai.api_key = os.getenv("OPENAI_API_KEY")
        embeddings = openai.Embedding.create(
            input=reasons, model="text-embedding-ada-002"
        )
        # Embedding API returns list of dicts with {'embedding': [...]}; extract the vectors
        return [emb["embedding"] for emb in embeddings["data"]]
    elif PROVIDER == "google":
        from google.cloud import generativeai as genai

        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        model = genai.models.Embedding("textembedding-gecko@001")
        results = model.embed_content(reasons)
        return [result.embeddings[0].values() for result in results]
    else:
        raise ValueError(f"Unsupported embedding provider: {PROVIDER}")


# Helper to embed a single reason (called by embed_reasons)
# def embed_single(reason: str) -> list:
#     # Implementation mirrors embed_reasons for a single item
#     pass

# Example usage (would be in a separate script):
# rationales = ["Harassment detected", "Self-harm content suspected"]
# vectors = embed_reasons(rationales)
# print(vectors)
