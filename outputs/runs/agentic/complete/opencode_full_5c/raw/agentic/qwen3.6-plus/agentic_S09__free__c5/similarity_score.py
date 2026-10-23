from typing import List
from openai import OpenAI
from embeddings_client import build_embeddings_client, load_config_from_env
from embeddings_models import SimilarityResult, cosine_similarity


def similarity_score(
    text_a: str, text_b: str, model: str = "text-embedding-3-small"
) -> SimilarityResult:
    config = load_config_from_env()
    client: OpenAI = build_embeddings_client(api_key=config["api_key"])
    response = client.embeddings.create(
        model=model,
        input=[text_a, text_b],
        encoding_format="float",
    )
    sorted_data = sorted(response.data, key=lambda x: x.index)
    embedding_a = sorted_data[0].embedding
    embedding_b = sorted_data[1].embedding
    sim = cosine_similarity(embedding_a, embedding_b)
    return SimilarityResult(
        text_a=text_a,
        text_b=text_b,
        similarity=sim,
        embedding_a=embedding_a,
        embedding_b=embedding_b,
    )


def compute_similarity_from_embeddings(
    embedding_a: List[float], embedding_b: List[float]
) -> float:
    return cosine_similarity(embedding_a, embedding_b)


if __name__ == "__main__":
    result = similarity_score("The cat sat on the mat", "A feline rested on the rug")
    print(f"Similarity: {result.similarity:.4f}")
