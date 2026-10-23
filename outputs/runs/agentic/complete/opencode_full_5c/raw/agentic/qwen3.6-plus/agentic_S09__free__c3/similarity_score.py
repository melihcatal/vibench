from embeddings_client import (
    get_openai_client,
    build_embedding_payload,
    extract_embedding_from_response,
)
from embeddings_models import (
    EmbeddingRequest,
    SimilarityResult,
    cosine_similarity,
    OPENAI_EMBEDDING_MODEL,
)


def similarity_score(
    text_a, text_b, model=OPENAI_EMBEDDING_MODEL, dimensions=1536, api_key=None
):
    client = get_openai_client(api_key=api_key)
    payload = build_embedding_payload(
        model=model,
        input_text=[text_a, text_b],
        dimensions=dimensions,
    )
    response = client.embeddings.create(**payload)
    vec_a = extract_embedding_from_response(response, index=0)
    vec_b = extract_embedding_from_response(response, index=1)
    sim = cosine_similarity(vec_a, vec_b)
    return SimilarityResult(text_a=text_a, text_b=text_b, similarity=sim)


if __name__ == "__main__":
    import sys

    if len(sys.argv) >= 3:
        a, b = sys.argv[1], sys.argv[2]
    else:
        a, b = "The cat sat on the mat", "A feline rested on a rug"
    result = similarity_score(a, b)
    print(f"Similarity: {result.similarity:.4f}")
    print(f"Text A: {result.text_a}")
    print(f"Text B: {result.text_b}")
