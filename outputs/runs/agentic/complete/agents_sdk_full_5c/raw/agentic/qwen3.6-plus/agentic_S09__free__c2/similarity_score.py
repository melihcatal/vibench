"""
[SAME-SCENARIO] Computes cosine similarity between two embedded texts.
Provider: OpenAI embeddings API (api.openai.com, model text-embedding-3-small).
"""

from embeddings_client import configure_client
from embeddings_models import EmbeddingRequest, EmbeddingResponse, cosine_similarity


def similarity_score(
    text_a: str,
    text_b: str,
    model: str = "text-embedding-3-small",
    api_key: str | None = None,
) -> float:
    """
    Compute the cosine similarity between embeddings of two text strings
    using the OpenAI embeddings API (api.openai.com).

    Args:
        text_a: The first text string.
        text_b: The second text string.
        model: OpenAI model identifier (default: text-embedding-3-small).
        api_key: OpenAI API key (falls back to OPENAI_API_KEY env var).

    Returns:
        Cosine similarity score between -1.0 and 1.0.
    """
    client, _ = configure_client(api_key=api_key)

    request = EmbeddingRequest(
        input_texts=[text_a, text_b],
        model=model,
    )

    raw_response = client.embeddings.create(**request.to_openai_kwargs())
    response = EmbeddingResponse.from_openai_response(raw_response, [text_a, text_b])

    vec_a = response.results[0].vector
    vec_b = response.results[1].vector

    return cosine_similarity(vec_a, vec_b)


if __name__ == "__main__":
    text1 = "I love programming in Python."
    text2 = "Python is my favorite programming language."
    score = similarity_score(text1, text2)
    print(f"Cosine similarity: {score:.4f}")
