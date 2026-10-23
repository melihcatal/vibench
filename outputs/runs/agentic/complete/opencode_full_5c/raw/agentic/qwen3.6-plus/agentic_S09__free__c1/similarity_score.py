from embeddings_client import get_openai_client, get_embedding_model
from embeddings_models import cosine_similarity


def similarity_score(text_a: str, text_b: str) -> float:
    client = get_openai_client()
    model = get_embedding_model()

    api_response = client.embeddings.create(
        model=model,
        input=[text_a, text_b],
        encoding_format="float",
    )

    vec_a = api_response.data[0].embedding
    vec_b = api_response.data[1].embedding

    return cosine_similarity(vec_a, vec_b)


if __name__ == "__main__":
    score = similarity_score("The cat sat on the mat", "A feline rested on the rug")
    print(f"Similarity score: {score:.4f}")
